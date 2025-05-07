import os
import logging
import random
from typing import Optional, Tuple
import contextlib

from mxlite import get_mxa_path
import asyncssh


logger = logging.getLogger("deployer")
service_file = "/etc/systemd/system/mxa.service"
# 修改服务内容为模板, 插入运行参数
service_content_template = """
[Unit]
Description=MXA Service
After=network.target
[Service]
ExecStart=/usr/local/bin/mxa {run_args}
Restart=always
[Install]
WantedBy=multi-user.target
"""


class MXADeployer:
    """MXA部署类, 使用 SSH 获取操作系统基础信息并部署 MXA"""

    def __init__(
        self,
        ssh_host: str,
        ssh_user: str,
        ssh_password: Optional[str] = None,
        ssh_key: Optional[str] = None,
    ):
        """
        初始化MXA部署类

        Args:
            ssh_host: SSH主机地址
            ssh_user: SSH用户名
            ssh_password: SSH密码
            ssh_key: SSH 密钥文件路径
        """
        self.ssh_host = ssh_host
        self.ssh_user = ssh_user
        self.ssh_password = ssh_password
        self.ssh_key = ssh_key
        self._connection = None  # 存储SSH连接
        self._port_forwards = {}  # 存储活跃的端口转发

        # 检查认证信息
        if not ssh_password and not ssh_key:
            raise ValueError("必须提供SSH密码或SSH密钥")

        if ssh_key and not os.path.isfile(ssh_key):
            raise ValueError(f"SSH密钥文件不存在: {ssh_key}")

    async def __aenter__(self):
        """实现异步上下文管理器入口"""
        if not self._connection:
            self._connection = await self._create_ssh_connection()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """实现异步上下文管理器出口"""
        # 停止所有端口转发
        await self.stop_all_forwards()

        # 关闭SSH连接
        if self._connection:
            self._connection.close()
            await self._connection.wait_closed()
            self._connection = None

    async def _create_ssh_connection(self):
        """
        创建SSH连接

        Returns:
            asyncssh.SSHClientConnection: SSH连接对象
        """
        try:
            if self.ssh_key:
                conn = await asyncssh.connect(
                    host=self.ssh_host,
                    username=self.ssh_user,
                    client_keys=[self.ssh_key],
                    known_hosts=None,
                )
            else:
                conn = await asyncssh.connect(
                    host=self.ssh_host,
                    username=self.ssh_user,
                    password=self.ssh_password,
                    known_hosts=None,
                )
            return conn
        except (asyncssh.Error, OSError) as e:
            logger.error(f"SSH连接失败: {str(e)}")
            raise e

    async def get_connection(self):
        """
        获取SSH连接, 如果不存在则创建

        Returns:
            asyncssh.SSHClientConnection: SSH连接对象
        """
        if not self._connection:
            self._connection = await self._create_ssh_connection()
        return self._connection

    @contextlib.asynccontextmanager
    async def connection(self):
        """
        连接上下文管理器, 提供一种更优雅的方式使用连接
        注意：此方法不会在退出上下文时关闭连接, 只有在连接出现问题时才会重置连接

        Yields:
            asyncssh.SSHClientConnection: SSH连接对象
        """
        conn = await self.get_connection()
        try:
            yield conn
        except asyncssh.Error as e:
            # 只有当连接出现SSH错误时, 才重置连接
            logger.error(f"SSH连接出错, 将重置连接: {str(e)}")
            if self._connection:
                self._connection.close()
                await self._connection.wait_closed()
                self._connection = None
            raise e

    async def close(self):
        """关闭SSH连接和所有端口转发"""
        # 停止所有端口转发
        await self.stop_all_forwards()

        # 关闭SSH连接
        if self._connection:
            self._connection.close()
            await self._connection.wait_closed()
            self._connection = None

    async def detect_arch(self) -> str:
        """
        通过 SSH 运行 Shell 脚本检测操作系统架构

        Returns:
            str: 操作系统架构信息
        """
        script = "uname -m"

        try:
            async with self.connection() as conn:
                result = await conn.run(script)

                # 处理架构信息
                arch = result.stdout.strip()

                # 转换为标准架构名称
                if arch in ["x86_64", "amd64"]:
                    return "x86_64"
                elif arch in ["aarch64", "arm64"]:
                    return "arm64"
                else:
                    return arch
        except asyncssh.Error as e:
            logger.error(f"执行架构检测脚本失败: {str(e)}")
            raise e

    async def detect_sudo(self) -> bool:
        """
        检测是否有 sudo 权限

        Returns:
            bool: 是否有 sudo 权限
        """
        script = "sudo -n true"

        try:
            async with self.connection() as conn:
                result = await conn.run(script)

                if result.exit_status == 0:
                    return True
                else:
                    return False
        except asyncssh.Error as e:
            logger.error(f"执行sudo检测脚本失败: {str(e)}")
            raise e
        except OSError as e:
            logger.error(f"SSH连接失败: {str(e)}")
            raise e
        except Exception as e:
            logger.error(f"未知错误: {str(e)}")
            raise e

    async def deploy_mxa(self) -> bool:
        """
        部署 MXA 到远程主机

        Returns:
            bool: 部署是否成功
        """

        try:
            # 检测是否有 sudo 权限
            has_sudo = await self.detect_sudo()
            if not has_sudo:
                logger.error("没有sudo权限, 无法继续部署")
                return False

            # 检测远程主机架构
            arch = await self.detect_arch()
            logger.info(f"检测到远程主机架构: {arch}")

            # 获取本地MXA路径
            mxa_path = get_mxa_path(arch)
            if not os.path.isfile(mxa_path):
                logger.error(f"未找到匹配的MXA可执行文件: {mxa_path}")
                return False

            # 使用连接池中的连接
            async with self.connection() as conn:
                try:
                    # 使用/tmp目录存放临时文件
                    temp_mxa_path = f"/tmp/mxa_temp_{os.getpid()}"

                    # 使用SFTP上传到临时目录
                    logger.info(f"开始上传MXA到临时位置: {temp_mxa_path}")
                    async with conn.start_sftp_client() as sftp:
                        await sftp.put(mxa_path, temp_mxa_path)

                    # 使用 sudo 将文件移动到系统目录
                    remote_dir = "/usr/local/bin"
                    mkdir_cmd = f"sudo mkdir -p {remote_dir}"
                    await conn.run(mkdir_cmd)

                    # 复制到系统目录并设置可执行权限
                    remote_mxa_path = f"{remote_dir}/mxa"
                    mv_cmd = f"sudo mv {temp_mxa_path} {remote_mxa_path} && sudo chmod +x {remote_mxa_path}"
                    mv_result = await conn.run(mv_cmd)
                    logger.debug(f"移动文件结果: {mv_result.stdout} {mv_result.stderr}")

                    # 验证安装
                    result = await conn.run("sudo mxa --version")
                    if result.exit_status == 0:
                        logger.info(f"MXA部署成功: {result.stdout.strip()}")
                        return True
                    else:
                        logger.error(f"MXA部署验证失败: {result.stderr.strip()}")
                        return False
                except Exception as e:
                    logger.error(f"MXA部署操作失败: {str(e)}")
                    return False
        except (asyncssh.Error, OSError) as e:
            logger.error(f"MXA部署失败: {str(e)}")
            return False

    async def create_port_forward(
        self, local_port: int, remote_host: str, remote_port: int
    ) -> Optional[asyncssh.SSHListener]:
        """
        创建从远程端口到本地主机端口的TCP转发
        这里使用forward_remote_port, 将远程服务器的端口转发到本地

        Args:
            local_port: 本地端口
            remote_host: 远程主机地址(通常为"localhost"或本地可访问的主机)
            remote_port: 远程服务器上的端口

        Returns:
            Optional[asyncssh.SSHListener]: 端口转发监听器, 如果创建失败则返回None
        """
        try:
            # 确保连接存在
            conn = await self.get_connection()

            # 创建端口转发 - 将远程端口转发到本地
            # 修改：确保监听在0.0.0.0而不是默认的localhost，这样远程的进程可以连接
            listener = await conn.forward_remote_port(
                "0.0.0.0", remote_port, remote_host, local_port
            )

            # 保存转发到字典中, 以便后续管理
            forward_key = f"{local_port}:{remote_host}:{remote_port}"
            self._port_forwards[forward_key] = listener

            logger.info(f"端口转发已创建: 远程{remote_port} -> 本地{local_port}")
            return listener

        except (asyncssh.Error, OSError) as e:
            logger.error(f"创建端口转发失败: {str(e)}")
            return None

    async def stop_port_forward(
        self, local_port: int, remote_host: str, remote_port: int
    ) -> bool:
        """
        停止特定的端口转发

        Args:
            local_port: 本地端口
            remote_host: 远程主机地址
            remote_port: 远程端口

        Returns:
            bool: 是否成功停止转发
        """
        forward_key = f"{local_port}:{remote_host}:{remote_port}"
        listener = self._port_forwards.get(forward_key)

        if listener:
            listener.close()
            del self._port_forwards[forward_key]
            logger.info(
                f"端口转发已停止: 本地{local_port} -> {remote_host}:{remote_port}"
            )
            return True
        else:
            logger.warning(
                f"未找到要停止的端口转发: 本地{local_port} -> {remote_host}:{remote_port}"
            )
            return False

    async def stop_all_forwards(self) -> None:
        """停止所有活跃的端口转发"""
        for key, listener in list(self._port_forwards.items()):
            listener.close()
            logger.info(f"端口转发已停止: {key}")

        self._port_forwards.clear()

    async def _get_random_remote_port(
        self, start: int = 30000, end: int = 40000
    ) -> int:
        """
        获取一个可用的随机远程端口

        Args:
            start: 端口范围起始值
            end: 端口范围结束值

        Returns:
            int: 可用的随机端口
        """
        # 生成随机端口
        random_port = random.randint(start, end)

        # 检查端口是否被占用
        try:
            async with self.connection() as conn:
                # 检查端口是否被占用 (netstat或ss命令)
                cmd = f"netstat -tuln | grep {random_port} || ss -tuln | grep {random_port}"
                result = await conn.run(cmd)

                # 如果输出非空, 说明端口被占用, 递归调用自身再次尝试
                if result.stdout.strip() or result.stderr.strip():
                    return await self._get_random_remote_port(start, end)

                return random_port
        except Exception as e:
            logger.error(f"检查远程端口时出错: {str(e)}")
            # 如果出错, 返回一个随机端口, 可能不安全, 但避免阻塞
            return random_port

    async def systemd_run_mxa(
        self,
        discovery_mode: bool = True,
        local_mxd_port: int = 8080,
        ws_url: Optional[str] = None,
    ) -> Tuple[bool, Optional[int]]:
        """
        使用 systemd 运行 MXA, 支持三种模式：
        1. 自动发现模式：MXA自动扫描网络寻找MXD
        2. 直连模式(使用端口转发)：MXA通过WebSocket连接到通过端口转发的MXD
        3. 直连模式(指定地址)：MXA通过WebSocket直接连接到指定URL

        Args:
            discovery_mode: 是否使用自动发现模式, False时使用直连模式
            local_mxd_port: 本地MXD的HTTP端口, 直连转发模式下使用
            ws_url: WebSocket URL, 如果提供则直接使用此URL, 忽略discovery_mode和local_mxd_port

        Returns:
            Tuple[bool, Optional[int]]: (是否成功运行, 如果使用端口转发则返回远程端口号)
        """
        try:
            forwarded_port = None

            # 确定运行参数
            run_args = ""

            # 优先使用提供的WebSocket URL
            if ws_url:
                run_args = f"-w {ws_url}"
                logger.info(f"MXA将使用直连模式连接到指定URL: {ws_url}")
            elif not discovery_mode:
                # 直连模式: 需要端口转发
                forwarded_port = await self._get_random_remote_port()

                # 创建端口转发: 将远程服务器的端口转发到本地MXD
                # 修改转发参数：确保本地监听在所有接口上，使用localhost作为远程主机
                listener = await self.create_port_forward(
                    local_port=local_mxd_port,
                    remote_host="localhost",
                    remote_port=forwarded_port,
                )

                if not listener:
                    logger.error("创建端口转发失败，无法启动MXA")
                    return False, None

                # 设置WebSocket连接参数 - 确保使用正确的协议和路径
                ws_url = f"ws://127.0.0.1:{forwarded_port}/ws"
                run_args = f"-w {ws_url}"
                logger.info(f"MXA将使用直连模式连接到: {ws_url}")
            else:
                logger.info("MXA将使用自动发现模式运行")

            # 填充服务文件内容
            service_content = service_content_template.format(run_args=run_args)

            # 创建 systemd 服务文件
            async with self.connection() as conn:
                # 使用 tee 命令写入 systemd 服务文件
                logger.info(f"使用 tee 写入 systemd 服务文件到: {service_file}")
                # 使用 sudo tee 来写入需要 root 权限的文件
                write_cmd = f"echo '{service_content}' | sudo tee {service_file}"
                result = await conn.run(
                    write_cmd, check=True
                )  # check=True 会在命令失败时抛出异常
                logger.debug(
                    f"写入 systemd 服务文件结果: {result.stdout} {result.stderr}"
                )

                await conn.run("sudo systemctl daemon-reload")  # 重新加载 systemd 配置
                await conn.run("sudo systemctl stop mxa || true")  # 确保停止已有服务
                await conn.run("sudo systemctl start mxa")  # 启动服务
                await conn.run("sudo systemctl enable mxa")  # 设置开机自启

            mode_desc = "自动发现" if discovery_mode and not ws_url else "直连"
            logger.info(f"MXA服务已成功启动并设置为开机自启, 模式: {mode_desc}")
            return True, forwarded_port
        except (asyncssh.Error, OSError) as e:
            logger.error(f"MXA服务启动失败: {str(e)}")
            # 如果失败, 尝试清理端口转发
            if not discovery_mode and forwarded_port and not ws_url:
                await self.stop_port_forward(
                    local_mxd_port, "127.0.0.1", forwarded_port
                )
            return False, None
        except Exception as e:
            logger.error(f"MXA服务操作失败: {str(e)}")
            return False, None
        finally:
            # 清理临时文件
            try:
                async with self.connection() as conn:
                    cleanup_cmd = "sudo rm -f /tmp/mxa_temp_*"
                    await conn.run(cleanup_cmd)
            except Exception as e:
                logger.error(f"清理临时文件失败: {str(e)}")

    async def systemd_remove_mxa(self) -> bool:
        """
        使用 systemd 移除 MXA

        Returns:
            bool: 是否成功移除
        """
        try:
            async with self.connection() as conn:
                await conn.run("sudo systemctl stop mxa")
                await conn.run("sudo systemctl disable mxa")
                await conn.run(f"sudo rm -f {service_file}")
                await conn.run("sudo systemctl daemon-reload")

            logger.info("MXA服务已成功停止并删除")
            return True
        except (asyncssh.Error, OSError) as e:
            logger.error(f"MXA服务移除失败: {str(e)}")
            return False
        except Exception as e:
            logger.error(f"MXA服务操作失败: {str(e)}")
            return False
