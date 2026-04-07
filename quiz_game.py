"""QuizGame 클래스 모듈 — 게임 전체를 관리하는 클래스"""

import json
import os
import random
from datetime import datetime

from quiz import Quiz


class QuizGame:
    """게임 전체를 관리하는 클래스

    Attributes:
        quizzes: 퀴즈 목록
        best_score: 최고 점수
        score_history: 점수 기록 히스토리
    """

    DATA_FILE = "state.json"

    def __init__(self):
        self.quizzes: list[Quiz] = []
        self.best_score: int = 0
        self.score_history: list[dict] = []
        self.load_data()

    # ── 기본 퀴즈 데이터 ──

    def get_default_quizzes(self) -> list[Quiz]:
        """기본 애니메이션 퀴즈 데이터 7개를 반환한다."""
        return [
            Quiz(
                question="나루토가 가진 미수의 이름은?",
                choices=["구미", "팔미", "이치비", "사비"],
                answer=1,
                hint="아홉 개의 꼬리를 가진 여우입니다",
            ),
            Quiz(
                question="루피가 먹은 악마의 열매는?",
                choices=["고무고무 열매", "불불 열매", "꽃꽃 열매", "어둠어둠 열매"],
                answer=1,
                hint="몸이 고무처럼 늘어납니다",
            ),
            Quiz(
                question="쿠로사키 이치고의 참백도 이름은?",
                choices=["천본앵", "참월", "햐쿠야", "와비스케"],
                answer=2,
                hint="'베어가르다'라는 의미입니다",
            ),
            Quiz(
                question="고죠 사토루의 술식 이름은?",
                choices=["영역전개", "무량공처", "무한", "육안"],
                answer=3,
                hint="이 술식은 수렴과 발산을 다루며 모든 것을 통과시키지 않습니다",
            ),
            Quiz(
                question="손오공이 변신하는 전설의 형태는?",
                choices=["기어 세컨드", "만화경 사륜안", "슈퍼 사이어인", "만해"],
                answer=3,
                hint="머리카락이 금색으로 변합니다",
            ),
            Quiz(
                question="에렌 예거가 가진 거인의 힘이 아닌 것은?",
                choices=["진격의 거인", "시조의 거인", "갑옷거인", "전쟁의 망치 거인"],
                answer=3,
                hint="갑옷거인은 라이너 브라운이 가지고 있습니다",
            ),
            Quiz(
                question="카마도 탄지로가 사용하는 호흡법의 이름은?",
                choices=["물의 호흡", "불의 호흡", "바람의 호흡", "해의 호흡"],
                answer=4,
                hint="탄지로의 아버지가 추던 신악의 춤과 관련이 있습니다",
            ),
        ]

    # ── 데이터 관리 ──

    def save_data(self) -> None:
        """퀴즈 데이터, 최고 점수, 히스토리를 state.json에 저장한다."""
        data = {
            "quizzes": [quiz.to_dict() for quiz in self.quizzes],
            "best_score": self.best_score,
            "score_history": self.score_history,
        }
        try:
            with open(self.DATA_FILE, "w", encoding="utf-8") as f:
                json.dump(data, f, ensure_ascii=False, indent=4)
        except IOError as e:
            print(f"⚠️ 데이터 저장 중 오류가 발생했습니다: {e}")

    def load_data(self) -> None:
        """state.json에서 데이터를 불러온다.

        파일이 없으면 기본 퀴즈로 시작하고,
        파일이 손상되었으면 안내 후 기본 데이터로 복구한다.
        """
        if not os.path.exists(self.DATA_FILE):
            self.quizzes = self.get_default_quizzes()
            return

        try:
            with open(self.DATA_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)

            self.quizzes = [Quiz.from_dict(q) for q in data.get("quizzes", [])]
            self.best_score = data.get("best_score", 0)
            self.score_history = data.get("score_history", [])

            if not self.quizzes:
                self.quizzes = self.get_default_quizzes()

        except (json.JSONDecodeError, KeyError, TypeError) as e:
            print(f"⚠️ 데이터 파일이 손상되었습니다: {e}")
            print("📂 기본 퀴즈 데이터로 복구합니다.")
            self.quizzes = self.get_default_quizzes()
            self.best_score = 0
            self.score_history = []

    # ── 유틸리티 ──

    def get_valid_input(self, prompt: str, min_val: int, max_val: int) -> int:
        """유효한 숫자 입력을 받을 때까지 반복한다.

        Args:
            prompt: 입력 안내 메시지
            min_val: 허용 최솟값
            max_val: 허용 최댓값

        Returns:
            유효한 정수 입력값
        """
        while True:
            try:
                user_input = input(prompt).strip()
                if not user_input:
                    print(f"⚠️ 입력이 비어 있습니다. {min_val}-{max_val} 사이의 숫자를 입력하세요.")
                    continue
                value = int(user_input)
                if min_val <= value <= max_val:
                    return value
                print(f"⚠️ 잘못된 입력입니다. {min_val}-{max_val} 사이의 숫자를 입력하세요.")
            except ValueError:
                print(f"⚠️ 잘못된 입력입니다. {min_val}-{max_val} 사이의 숫자를 입력하세요.")

    # ── 메뉴 ──

    def show_menu(self) -> None:
        """메뉴를 출력한다."""
        print()
        print("========================================")
        print("      🎯 애니메이션 퀴즈 게임 🎯")
        print("========================================")
        print(f"  📂 퀴즈 {len(self.quizzes)}개 | 🏆 최고 {self.best_score}점")
        print("----------------------------------------")
        print("  1. 퀴즈 풀기")
        print("  2. 퀴즈 추가")
        print("  3. 퀴즈 목록")
        print("  4. 퀴즈 삭제")
        print("  5. 점수 확인")
        print("  6. 종료")
        print("========================================")

    # ── 핵심 기능 (Phase 4~5에서 구현) ──

    def play_quiz(self) -> None:
        """퀴즈를 출제하고 결과를 표시한다."""
        if not self.quizzes:
            print("\n❌ 등록된 퀴즈가 없습니다. 먼저 퀴즈를 추가해주세요.")
            return

        # 문제 수 선택
        total = len(self.quizzes)
        print(f"\n📝 등록된 퀴즈: {total}개")
        count = self.get_valid_input(
            f"몇 문제를 풀겠습니까? (1-{total}): ", 1, total
        )

        # 랜덤 출제
        selected = random.sample(self.quizzes, count)

        print(f"\n🚀 퀴즈를 시작합니다! 즐거운 시간 되세요! (총 {count}문제)")
        print("💡 힌트를 보려면 0을 입력하세요.")

        correct = 0
        hints_used = 0

        for i, quiz in enumerate(selected, 1):
            quiz.display(number=i)

            hint_used_this = False

            while True:
                try:
                    user_input = input("정답 입력 (0: 힌트): ").strip()
                    if not user_input:
                        print("⚠️ 입력이 비어 있습니다. 1-4 사이의 숫자를 입력하세요.")
                        continue
                    value = int(user_input)
                    if value == 0:
                        if hint_used_this:
                            print("💡 이미 힌트를 확인했습니다.")
                        else:
                            quiz.display_hint()
                            hint_used_this = True
                            hints_used += 1
                        continue
                    if 1 <= value <= 4:
                        break
                    print("⚠️ 잘못된 입력입니다. 1-4 사이의 숫자를 입력하세요.")
                except ValueError:
                    print("⚠️ 잘못된 입력입니다. 1-4 사이의 숫자를 입력하세요.")

            if quiz.check_answer(value):
                if hint_used_this:
                    correct += 0.5
                    print("✅ 정답입니다! (힌트 사용으로 0.5점)")
                else:
                    correct += 1
                    print("✅ 정답입니다!")
            else:
                print(f"❌ 오답입니다. 정답은 {quiz.answer}번 '{quiz.choices[quiz.answer - 1]}'입니다.")

        # 결과 표시
        score = int(correct / count * 100)
        print()
        print("========================================")
        print(f"🏆 결과: {count}문제 중 {correct}문제 정답! ({score}점)")

        if score > self.best_score:
            self.best_score = score
            print("🎉 새로운 최고 점수입니다!")

        print("========================================")

        # 히스토리 기록
        record = {
            "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "total_questions": count,
            "correct_answers": correct,
            "score": score,
            "hints_used": hints_used,
        }
        self.score_history.append(record)
        self.save_data()

    def add_quiz(self) -> None:
        """사용자로부터 새로운 퀴즈를 입력받아 추가한다."""
        print("\n📌 새로운 퀴즈를 추가합니다.\n")

        question = ""
        while not question:
            question = input("문제를 입력하세요: ").strip()
            if not question:
                print("⚠️ 문제를 입력해주세요.")

        choices = []
        for i in range(1, 5):
            choice = ""
            while not choice:
                choice = input(f"선택지 {i}: ").strip()
                if not choice:
                    print("⚠️ 선택지를 입력해주세요.")
            choices.append(choice)

        answer = self.get_valid_input("정답 번호 (1-4): ", 1, 4)

        hint = input("힌트를 입력하세요 (없으면 Enter): ").strip()

        quiz = Quiz(question=question, choices=choices, answer=answer, hint=hint)
        self.quizzes.append(quiz)
        self.save_data()

        print("\n✅ 퀴즈가 추가되었습니다!")

    def list_quizzes(self) -> None:
        """등록된 퀴즈 목록을 출력한다."""
        if not self.quizzes:
            print("\n❌ 등록된 퀴즈가 없습니다.")
            return

        print(f"\n📋 등록된 퀴즈 목록 (총 {len(self.quizzes)}개)")
        print("----------------------------------------")
        for i, quiz in enumerate(self.quizzes, 1):
            print(f"[{i}] {quiz.question}")
        print("----------------------------------------")

    def delete_quiz(self) -> None:
        """등록된 퀴즈를 삭제한다."""
        if not self.quizzes:
            print("\n❌ 등록된 퀴즈가 없습니다.")
            return

        self.list_quizzes()
        index = self.get_valid_input(
            f"\n삭제할 퀴즈 번호를 입력하세요 (1-{len(self.quizzes)}): ",
            1,
            len(self.quizzes),
        )

        deleted = self.quizzes.pop(index - 1)
        print(f"\n🗑️ 삭제되었습니다: {deleted.question}")
        self.save_data()

    def show_score(self) -> None:
        """최고 점수와 히스토리를 출력한다."""
        print()
        print("========================================")
        if self.best_score > 0:
            print(f"🏆 최고 점수: {self.best_score}점")
        else:
            print("🏆 아직 퀴즈를 풀지 않았습니다.")

        if self.score_history:
            print()
            print("📊 최근 플레이 기록:")
            print("----------------------------------------")
            for record in self.score_history[-5:]:
                date = record.get("date", "알 수 없음")
                total = record.get("total_questions", 0)
                correct = record.get("correct_answers", 0)
                score = record.get("score", 0)
                hints = record.get("hints_used", 0)
                print(f"  {date} | {total}문제 중 {correct}정답 | {score}점 | 힌트 {hints}회")
            print("----------------------------------------")

        print("========================================")

    # ── 메인 루프 ──

    def run(self) -> None:
        """메인 게임 루프를 실행한다."""
        # 시작 시 데이터 로드 안내
        quiz_count = len(self.quizzes)
        if os.path.exists(self.DATA_FILE):
            print(f"\n📂 저장된 데이터를 불러왔습니다. (퀴즈 {quiz_count}개, 최고점수 {self.best_score}점)")
        else:
            print(f"\n📂 기본 퀴즈 데이터로 시작합니다. (퀴즈 {quiz_count}개)")

        try:
            while True:
                self.show_menu()
                choice = self.get_valid_input("선택: ", 1, 6)

                if choice == 1:
                    self.play_quiz()
                elif choice == 2:
                    self.add_quiz()
                elif choice == 3:
                    self.list_quizzes()
                elif choice == 4:
                    self.delete_quiz()
                elif choice == 5:
                    self.show_score()
                elif choice == 6:
                    self.save_data()
                    print("\n👋 게임을 종료합니다. 데이터가 저장되었습니다.")
                    break

        except KeyboardInterrupt:
            self.save_data()
            print("\n\n👋 Ctrl+C가 감지되었습니다. 데이터를 저장하고 종료합니다.")
        except EOFError:
            self.save_data()
            print("\n\n👋 입력이 종료되었습니다. 데이터를 저장하고 종료합니다.")
