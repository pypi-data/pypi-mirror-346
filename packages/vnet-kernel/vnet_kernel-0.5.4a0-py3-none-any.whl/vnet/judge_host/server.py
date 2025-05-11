import logging
from ctypes import sizeof

from vnet.structs_mapper.gbn import ACKPacket, Packet

from .network_simulator import NetworkSimulator
from .socket_manager import SocketManager


def setup_logger(name, log_file=None):
    """设置并返回日志记录器"""
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)

    if log_file:
        file_handler = logging.FileHandler(log_file)
        formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)

    return logger


class UDPServer:
    def __init__(
        self,
        ipv4_addr: str = "127.0.0.1",
        host_name: str = "Reliable_Server",
        port: int = 8000,
        packet_loss_rate: float = 0.0,
        delay_ms: int = 0,
    ):
        self.ipv4_addr = ipv4_addr
        self.port = port
        self.host_name = host_name
        self.logger = setup_logger(f"{host_name}", f"{host_name.lower()}.log")
        self.network_simulator = NetworkSimulator(packet_loss_rate, delay_ms)
        self.socket_manager = SocketManager(ipv4_addr, port, self.logger)
        # 记录已接收的数据包序列号，用于去重
        self.received_seqs = set()

    def register_packet_handler(self, handler):
        """注册数据包处理函数"""
        self.socket_manager.register_packet_handler(handler)

    def start(self):
        """启动服务器"""
        self.socket_manager.initialize()
        self.socket_manager.start_listening()
        self.logger.info(f"{self.host_name} 服务器已启动")

    def stop(self):
        """停止服务器"""
        self.socket_manager.stop_listening()
        self.socket_manager.cleanup()
        self.logger.info(f"{self.host_name} 服务器已停止")

    def set_network_conditions(self, packet_loss_rate=None, delay_ms=None):
        """设置网络条件"""
        self.network_simulator.set_conditions(packet_loss_rate, delay_ms)
        self.logger.info(
            f"网络条件已更新: 丢包率={self.network_simulator.packet_loss_rate}, 延迟={self.network_simulator.delay_ms}ms"
        )

    def create_cli_socket(self):
        conn = self.socket_manager.create_client_socket(self.port)
        return conn

    def handle_gbn_packet(self, data: bytes, addr: tuple, socket_mgr):
        """handler,收到GBN数据包时的处理函数"""
        try:
            # 模拟网络条件，如果需要丢弃此包则直接返回
            if self.network_simulator.should_drop_packet():
                self.logger.info(f"模拟网络丢包，丢弃来自 {addr} 的数据包")
                return

            # 解析接收到的Packet结构
            if len(data) < sizeof(Packet):
                self.logger.error(f"数据包太小，无法解析: {len(data)} < {sizeof(Packet)}")
                return

            # 从数据中提取序号 - 第一个字节是序号
            seq = data[0]
            self.logger.info(f"收到SEQ序号为 {seq} 的数据包")

            # 创建正确的ACKPacket结构
            ack_packet = ACKPacket(seq)

            # 模拟网络延迟
            self.network_simulator.simulate_delay()

            # 发送正确格式的ACK包
            socket_mgr.send_packet(ack_packet, addr)
            self.logger.info(f"向 {addr} 发送ACK包: {ack_packet.ack}")

            # 记录已处理的序号
            self.received_seqs.add(seq)

        except Exception as e:
            self.logger.error(f"处理GBN数据包时出错: {e}")
