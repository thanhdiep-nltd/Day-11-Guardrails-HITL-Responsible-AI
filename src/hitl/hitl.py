"""
Lab 11 — Part 4: Human-in-the-Loop Design
  TODO 12: Confidence Router
  TODO 13: Design 3 HITL decision points
"""
from dataclasses import dataclass


# ============================================================
# TODO 12: Implement ConfidenceRouter
#
# Route agent responses based on confidence scores:
#   - HIGH (>= 0.9): Auto-send to user
#   - MEDIUM (0.7 - 0.9): Queue for human review
#   - LOW (< 0.7): Escalate to human immediately
#
# Special case: if the action is HIGH_RISK (e.g., money transfer,
# account deletion), ALWAYS escalate regardless of confidence.
#
# Implement the route() method.
# ============================================================

HIGH_RISK_ACTIONS = [
    "transfer_money",
    "close_account",
    "change_password",
    "delete_data",
    "update_personal_info",
]


@dataclass
class RoutingDecision:
    """Result of the confidence router."""
    action: str          # "auto_send", "queue_review", "escalate"
    confidence: float
    reason: str
    priority: str        # "low", "normal", "high"
    requires_human: bool


class ConfidenceRouter:
    """Route agent responses based on confidence and risk level.

    Thresholds:
        HIGH:   confidence >= 0.9 -> auto-send
        MEDIUM: 0.7 <= confidence < 0.9 -> queue for review
        LOW:    confidence < 0.7 -> escalate to human

    High-risk actions always escalate regardless of confidence.
    """

    HIGH_THRESHOLD = 0.9
    MEDIUM_THRESHOLD = 0.7

    def route(self, response: str, confidence: float,
              action_type: str = "general") -> RoutingDecision:
        """Route a response based on confidence score and action type.

        Args:
            response: The agent's response text
            confidence: Confidence score between 0.0 and 1.0
            action_type: Type of action (e.g., "general", "transfer_money")

        Returns:
            RoutingDecision with routing action and metadata
        """
        # 1. Check if action_type is in HIGH_RISK_ACTIONS
        if action_type in HIGH_RISK_ACTIONS:
            return RoutingDecision(
                action="escalate",
                confidence=confidence,
                reason=f"High-risk action: {action_type}",
                priority="high",
                requires_human=True,
            )

        # 2. Check confidence thresholds:
        if confidence >= self.HIGH_THRESHOLD:
            return RoutingDecision(
                action="auto_send",
                confidence=confidence,
                reason="High confidence",
                priority="low",
                requires_human=False,
            )
        elif self.MEDIUM_THRESHOLD <= confidence < self.HIGH_THRESHOLD:
            return RoutingDecision(
                action="queue_review",
                confidence=confidence,
                reason="Medium confidence — needs review",
                priority="normal",
                requires_human=True,
            )
        else:
            return RoutingDecision(
                action="escalate",
                confidence=confidence,
                reason="Low confidence — escalating",
                priority="high",
                requires_human=True,
            )


# ============================================================
# TODO 13: Design 3 HITL decision points
hitl_decision_points = [
    {
        "id": 1,
        "name": "Xác thực giao dịch chuyển tiền giá trị lớn",
        "trigger": "Khách hàng yêu cầu chuyển khoản một số tiền vượt quá 50,000,000 VND.",
        "hitl_model": "human-in-the-loop",
        "context_needed": "Thông tin chi tiết người gửi, số tài khoản thụ hưởng, số tiền, và lịch sử giao dịch gần đây của tài khoản gửi.",
        "example": "Người dùng yêu cầu chuyển 100,000,000 VND đến một tài khoản lạ lần đầu tiên xuất hiện trong danh bạ.",
    },
    {
        "id": 2,
        "name": "Xác nhận đóng tài khoản hoặc tất toán sổ tiết kiệm trước hạn",
        "trigger": "Yêu cầu từ người dùng muốn khóa tài khoản thanh toán hoặc rút toàn bộ tiền tiết kiệm sớm.",
        "hitl_model": "human-in-the-loop",
        "context_needed": "Thông tin định danh của chủ tài khoản, số dư hiện tại, lý do tất toán trước hạn, và kiểm tra cuộc gọi video xác minh (nếu có).",
        "example": "Khách hàng muốn tất toán gấp sổ tiết kiệm 500,000,000 VND trước hạn 6 tháng do nghi ngờ có cuộc gọi mạo danh cơ quan chức năng đe dọa.",
    },
    {
        "id": 3,
        "name": "Phát hiện hành vi trò chuyện bất thường hoặc có dấu hiệu leo thang tấn công",
        "trigger": "Hệ thống Guardrails phát hiện nhiều phản hồi bị chặn liên tiếp từ cùng một phiên người dùng hoặc điểm tin cậy LLM Judge đánh giá thấp (< 0.7).",
        "hitl_model": "human-on-the-loop",
        "context_needed": "Lịch sử cuộc hội thoại (chat logs) của phiên hiện tại, các cảnh báo guardrail đã kích hoạt, địa chỉ IP và lịch sử các lần đăng nhập gần đây.",
        "example": "Một tài khoản liên tục gửi các câu hỏi tìm cách khai thác thông tin cấu hình hệ thống bằng nhiều ngôn ngữ khác nhau trong thời gian ngắn.",
    },
]


# ============================================================
# Quick tests
# ============================================================

def test_confidence_router():
    """Test ConfidenceRouter with sample scenarios."""
    router = ConfidenceRouter()

    test_cases = [
        ("Balance inquiry", 0.95, "general"),
        ("Interest rate question", 0.82, "general"),
        ("Ambiguous request", 0.55, "general"),
        ("Transfer $50,000", 0.98, "transfer_money"),
        ("Close my account", 0.91, "close_account"),
    ]

    print("Testing ConfidenceRouter:")
    print("=" * 80)
    print(f"{'Scenario':<25} {'Conf':<6} {'Action Type':<18} {'Decision':<15} {'Priority':<10} {'Human?'}")
    print("-" * 80)

    for scenario, conf, action_type in test_cases:
        decision = router.route(scenario, conf, action_type)
        print(
            f"{scenario:<25} {conf:<6.2f} {action_type:<18} "
            f"{decision.action:<15} {decision.priority:<10} "
            f"{'Yes' if decision.requires_human else 'No'}"
        )

    print("=" * 80)


def test_hitl_points():
    """Display HITL decision points."""
    print("\nHITL Decision Points:")
    print("=" * 60)
    for point in hitl_decision_points:
        print(f"\n  Decision Point #{point['id']}: {point['name']}")
        print(f"    Trigger:  {point['trigger']}")
        print(f"    Model:    {point['hitl_model']}")
        print(f"    Context:  {point['context_needed']}")
        print(f"    Example:  {point['example']}")
    print("\n" + "=" * 60)


if __name__ == "__main__":
    test_confidence_router()
    test_hitl_points()
