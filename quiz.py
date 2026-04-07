"""Quiz 클래스 모듈 — 개별 퀴즈를 표현하는 클래스"""


class Quiz:
    """개별 퀴즈를 표현하는 클래스

    Attributes:
        question: 문제 텍스트
        choices: 선택지 4개 (리스트)
        answer: 정답 번호 (1~4)
        hint: 힌트 텍스트 (선택)
    """

    def __init__(self, question: str, choices: list[str], answer: int, hint: str = ""):
        self.question = question
        self.choices = choices
        self.answer = answer
        self.hint = hint

    def display(self, number: int = 0) -> None:
        """퀴즈 문제와 선택지를 화면에 출력

        Args:
            number: 문제 번호 (0이면 번호를 출력하지 않음)
        """
        print()
        print("----------------------------------------")
        if number > 0:
            print(f"[문제 {number}]")
        print(self.question)
        print()
        for i, choice in enumerate(self.choices, 1):
            print(f"  {i}. {choice}")
        print()

    def display_hint(self) -> None:
        """힌트를 출력한다. 힌트가 없으면 안내 메시지를 출력한다."""
        if self.hint:
            print(f"💡 힌트: {self.hint}")
        else:
            print("❌ 이 문제에는 힌트가 없습니다.")

    def check_answer(self, user_answer: int) -> bool:
        """사용자 답이 정답인지 확인한다.

        Args:
            user_answer: 사용자가 입력한 답 번호 (1~4)

        Returns:
            정답이면 True, 오답이면 False
        """
        return user_answer == self.answer

    def to_dict(self) -> dict:
        """JSON 직렬화를 위한 딕셔너리 변환

        Returns:
            퀴즈 데이터를 담은 딕셔너리
        """
        return {
            "question": self.question,
            "choices": self.choices,
            "answer": self.answer,
            "hint": self.hint,
        }

    @classmethod
    def from_dict(cls, data: dict) -> "Quiz":
        """딕셔너리에서 Quiz 인스턴스를 생성한다.

        Args:
            data: 퀴즈 데이터를 담은 딕셔너리

        Returns:
            Quiz 인스턴스
        """
        return cls(
            question=data["question"],
            choices=data["choices"],
            answer=data["answer"],
            hint=data.get("hint", ""),
        )
