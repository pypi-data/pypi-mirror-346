import chardet


def detect(file_name: str):
    file = open(file_name, "rb")

    detector = (
        chardet.UniversalDetector()
    )

    line = file.readline()

    while line:
        detector.feed(line)

        if detector.done:
            break

        line = file.readline()

    detector.close()

    file_encoding = detector.result[
        "encoding"
    ]

    file_encoding_confidence = (
        detector.result["confidence"]
    )

    print(
        "For file "
        + file_name
        + " encoding "
        + file_encoding
        + " with confidence "
        + str(file_encoding_confidence)
        + " was detected.",
    )

    return file_encoding
