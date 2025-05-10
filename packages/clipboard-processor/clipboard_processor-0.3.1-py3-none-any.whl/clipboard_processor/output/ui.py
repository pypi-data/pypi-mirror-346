from threading import Thread
from typing import Optional

import pyperclip

from clipboard_processor.output._base import Output

MAX_OPACITY = 0.8
MIN_OPACITY = 0.1
FADE_OUT_STEPS_PER_S = 10


class UiOutput(Output):

    @classmethod
    def name(cls):
        return 'ui'

    @classmethod
    def is_available(cls):
        return True

    def show(self, title: str, content: str, timeout: Optional[int] = None):
        def run_tk():
            import tkinter as tk
            from tkinter import ttk

            root = tk.Tk()
            frm = tk.Frame(root, background='black', padx=4, pady=4)

            root.attributes('-type', 'dialog')
            root.attributes('-topmost', True)
            root.attributes('-alpha', MAX_OPACITY)
            # name
            root.title('clipboard-processor')
            root.overrideredirect(True)
            abs_coord_x = root.winfo_pointerx() - root.winfo_vrootx()
            abs_coord_y = root.winfo_pointery() - root.winfo_vrooty()
            screen_width = root.winfo_screenwidth()
            screen_height = root.winfo_screenheight()

            def move_window():
                x = abs_coord_x + 10
                y = abs_coord_y + 10
                if x + frm.winfo_width() > screen_width:
                    x = screen_width - frm.winfo_width()
                if y + frm.winfo_height() > screen_height:
                    y = screen_height - frm.winfo_height()
                root.geometry(f'+{x}+{y}')

            frm.grid()
            label = ttk.Label(frm, text=title, background='black', foreground='white', font='TkSmallCaptionFont')
            label.grid(column=0, row=0, sticky='w')

            content_text = ttk.Label(frm, text=content.strip(), background='black', foreground='white',
                                     font='TkFixedFont')
            content_text.grid(column=0, row=1, sticky='w', pady=(4, 0))

            def copy_to_clipboard(_):
                pyperclip.copy(content)
                content_text.config(text=content.strip() + '\n<copied>')
                frm.pack()
                root.update()
                move_window()

            def destroy(*_, **__):
                root.destroy()

            def set_opacity(opacity):
                root.attributes('-alpha', opacity)
                root.update()

            for element in [frm, label, content_text]:
                element.bind('<Button-1>', destroy)
                element.bind('<Button-3>', copy_to_clipboard)

            frm.pack()
            root.update()
            move_window()
            if timeout:
                for i in range(FADE_OUT_STEPS_PER_S * timeout):
                    o = MAX_OPACITY - (MAX_OPACITY - MIN_OPACITY) * (i / (FADE_OUT_STEPS_PER_S * timeout)) ** 4
                    root.after(int(i * 1000 / FADE_OUT_STEPS_PER_S), set_opacity, o)

                root.after(timeout * 1000, destroy)

            root.mainloop()

        thread = Thread(target=run_tk, daemon=True)
        thread.start()
