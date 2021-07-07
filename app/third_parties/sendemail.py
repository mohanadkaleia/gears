import yagmail


class ErrNoContentFound(Exception):
    pass


# TODO: change this to dklube63
send_to = "ms.kaleia@gmail.com"


def send(subject, from_email="", content=None):
    if content is None:
        raise ErrNoContentFound("content is missing")

    subject = "DKLube | " + subject
    do_not_reply = "Do not reply to this message \n"

    # TODO: haha need to change this password here
    yag = yagmail.SMTP("mycodee.dev", "A54GzsbUgkZgHMsd")
    yag.send("ms.kaleia@gmail.com", subject, [do_not_reply, content])
