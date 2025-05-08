import tkinter


def create_textbox_with_label(
    master: tkinter.Tk,
    row: int,
    label_text: str,
    width: int,
) -> tkinter.Entry:
    label = tkinter.Label(
        master, text=label_text
    )
    label.grid(
        row=row, sticky=tkinter.W
    )

    textbox = tkinter.Entry(
        master, width=width
    )

    textbox.grid(
        row=row,
        column=1,
        sticky=tkinter.W,
    )

    return textbox


def create_text_with_label(
    master: tkinter.Tk,
    row: int,
    label_text: str,
    initial_list: list,
) -> tkinter.Text:
    label = tkinter.Label(
        master, text=label_text
    )
    label.grid(
        row=row, sticky=tkinter.W
    )

    text = tkinter.Text(
        master=master, height=3
    )

    for item in initial_list:
        text.insert(
            tkinter.INSERT, item + "\n"
        )

    text.grid(
        row=row,
        column=1,
        sticky=tkinter.W,
    )

    return text


def create_button(
    master: tkinter.Tk,
    button_text: str,
    command: callable,
    row: int,
):
    button = tkinter.Button(
        master,
        text=button_text,
        command=command,
    )

    button.grid(
        row=row,
        column=2,
        sticky=tkinter.W,
        pady=4,
    )
