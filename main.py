"""나만의 퀴즈 게임 — 엔트리포인트"""

from quiz_game import QuizGame


def main():
    """프로그램을 시작한다."""
    game = QuizGame()
    game.run()


if __name__ == "__main__":
    main()
