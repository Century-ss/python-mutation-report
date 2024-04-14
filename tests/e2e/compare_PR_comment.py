if __name__ == "__main__":
    with open("actual_PR_comment.txt", "r") as f:
        actual_PR_comment = f.read().rstrip()

    actual_PR_comment = actual_PR_comment[1:-1]
    actual_PR_comment = (
        actual_PR_comment.replace("\\n", "\n").replace('\\"', '"').replace("\\'", "'")
    )

    with open("tests/data/expected/PR_comment.txt", "r") as f:
        expected_PR_comment = f.read().rstrip()

    if actual_PR_comment != expected_PR_comment:
        raise ValueError("The pull request comments are not what is expected.")
