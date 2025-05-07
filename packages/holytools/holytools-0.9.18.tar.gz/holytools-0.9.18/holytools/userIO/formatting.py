class MessageFormatter:
    @staticmethod
    def get_boxed(text: str, headline: str = "") -> str:
        text = text.replace('\t', ' ' * 4)
        lines = text.split("\n")

        max_length = max([len(line) for line in lines] + [len(headline)+2])
        border = "+" + "-" * (max_length + 2) + "+"
        if headline:
            headline = f' {headline} '
            top_line = f"+{headline.center(max_length + 2, '-')}+"
        else:
            top_line =  border
        bottom_line = border

        boxed_lines = [top_line] + [f"| {line.ljust(max_length)} |" for line in lines] + [bottom_line]
        return "\n".join(boxed_lines) + '\n'

    @staticmethod
    def multi_section_box(texts: list[str], headlines: list[str]) -> str:
        combined_text = ''.join(texts)
        text = combined_text.replace('\t', ' ' * 4)
        lines = text.split("\n")

        max_length = max([len(line) for line in lines] + [len(h)+2 for h in headlines])
        border = "+" + "-" * (max_length + 2) + "+"

        lines = []
        for t, h in zip(texts, headlines):
            h = f' {h} '
            top_line = f"+{h.center(max_length + 2, '-')}+"
            lines += [top_line] + [f"| {line.ljust(max_length)} |" for line in t.split("\n")]
        lines += [border]

        return "\n".join(lines) + '\n'

    @staticmethod
    def get_boxed_train(messages: list) -> str:
        if len(messages) == 0:
            raise ValueError("No messages to format")

        for msg in messages:
            if '\n' in msg:
                raise ValueError(f"Message contains newline character: {msg}")
        wagons = [MessageFormatter.get_boxed(headline="", text=msg) for msg in messages]

        total_str = ''
        no_lines = 3
        wagon_sep = 5

        pulled_cabins = [w.split('\n') for w in wagons[:-1]]
        conductor_lines = wagons[-1].split('\n')

        for j in range(no_lines):
            connect_symbol = '-' if j == 1 else ' '
            connector = f'{connect_symbol * wagon_sep}'
            for lines in pulled_cabins:
                total_str += f'{lines[j]}{connector}'
            total_str += f'{conductor_lines[j]}\n'

        total_str = total_str.strip()

        return total_str
