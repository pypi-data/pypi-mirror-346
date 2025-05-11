import logging
import random
import time


class NetworkSimulator:
    """网络模拟器，用于模拟丢包和延迟"""

    def __init__(
        self, packet_loss_rate: float = 0.0, delay_ms: int = 0, seq_to_drop: list[int] | None = None
    ):
        self.packet_loss_rate = packet_loss_rate
        self.delay_ms = delay_ms
        self.logger = logging.getLogger("network_simulator")
        # drop packest with specified seq num
        self.seq_to_drop = seq_to_drop or []

    def set_conditions(self, packet_loss_rate=None, delay_ms=None):
        """设置网络条件"""
        if packet_loss_rate is not None:
            self.packet_loss_rate = max(0.0, min(1.0, packet_loss_rate))
        if delay_ms is not None:
            self.delay_ms = max(0, delay_ms)

    def should_drop_packet(self, seq_num=None) -> bool:
        """根据丢包率决定是否丢弃数据包"""
        if seq_num and seq_num in self.seq_to_drop:
            return True
        # drop packet with specified seq num
        drop = random.random() < self.packet_loss_rate
        if drop:
            self.logger.info("模拟丢包")
        return drop

    def simulate_delay(self):
        """模拟网络延迟"""
        if self.delay_ms > 0:
            time.sleep(self.delay_ms / 1000.0)
