from shiny import ui, reactive, render, App
from chemcrow.agents import ChemCrow
import asyncio
import shinyswatch
import html

chem_model = ChemCrow(model="gpt-4-0613", temp=0.1, verbose=True)

app_ui = ui.page_fluid(
    shinyswatch.theme.slate(),
    ui.panel_title("ChemCrow UI"),
    ui.p("An experiment with Shiny for Python and ChemCrow"),
    ui.br(),
    ui.row(
        ui.column(9, ui.input_text("prompt", label=None, placeholder="E.g., What is the molecular weight of tylenol?", width="100%")),
        ui.column(3, ui.input_action_button("chat", "Chat", class_="btn btn-primary btn-lg btn-block", width="100%"),)
    ),
    ui.output_text("txt"),
    ui.output_ui("prompt_ui"),
    ui.output_ui("result"),
    ui.hr(),
    ui.div(
        {"style": "align-items: center; display: flex; flex-direction: column; justify-content: center;"},
        ui.img(src="https://github.com/ur-whitelab/chemcrow-public/raw/main/assets/chemcrow_dark_thin.png", width="400px")
    ),
    ui.br(),
    ui.markdown(f'ChemCrow was [introduced](https://arxiv.org/abs/2304.05376) by Bran, Andres M., et al. "ChemCrow: Augmenting large-language models with chemistry tools." arXiv preprint arXiv:2304.05376 (2023). This tool is an extension of that work that puts the code into an interactive web app created by [James Wade](https://jameshwade.com) using [Shiny for Python](https://shiny.posit.co/py/). Find the code for the app [here](https://github.com/jameshwade/chemcrow) and the original code [here](https://github.com/ur-whitelab/chemcrow-public).')
)

def server(input, output, session):
    @reactive.Effect()
    def _():
        if input.chat():
            ui.update_text("prompt", value="")
    
    @output
    @render.ui
    @reactive.event(input.chat)
    def prompt_ui():
        list_ui = [ui.strong("Prompt"),
                   ui.markdown(input.prompt())]
        return list_ui

    @output
    @render.ui
    @reactive.event(input.chat) # triggered when the "Chat" button is clicked
    async def result():
        ui.notification_show("Chatting with ChemCrow...", type="message")
        try:
            response = await asyncio.to_thread(chem_model.run, input.prompt())
            list_ui = [ui.strong("Thoughts"),
                       ui.markdown(response[0]),
                       ui.strong("Reasoning"),
                       ui.markdown(response[1]),
                       ui.strong("Answer"),
                       ui.markdown(response[2])]
            return list_ui
        except TypeError:
            async def error_coro():
                return "An error occurred while processing your request."
            return await error_coro()

app = App(app_ui, server, debug=True)