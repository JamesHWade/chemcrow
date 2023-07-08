from shiny import ui, reactive, render, App
from chemcrow.agents import ChemCrow
import asyncio

chem_model = ChemCrow(model="gpt-4-0613", temp=0.1, verbose=True)

app_ui = ui.page_fluid(
    ui.h1("ChemCrow UI"),
    ui.h2("An experiment with Shiny and ChemCrow"),
    ui.br(),
    ui.row(
        ui.column(9, ui.input_text_area("prompt", label=None, placeholder="E.g., What is the molecular weight of tylenol?", width="100%", resize="both")),
        ui.column(3, ui.input_action_button("chat", "Chat", class_="btn btn-primary btn-lg btn-block", width="100%"),)
    ),
    ui.output_text("result"),
    ui.hr(),
    ui.div(
        {"style": "font-weight: bold;"},
        ui.img(src="https://github.com/ur-whitelab/chemcrow-public/raw/main/assets/chemcrow_light_thin.png", width="400px")
    ),
)


def server(input, output, session):
    @output
    @render.text
    def txt():
        return input.prompt()
    
    @output
    @render.text
    @reactive.event(input.chat) # triggered when the "Chat" button is clicked
    async def result():
        try:
            response = await asyncio.to_thread(chem_model.run, input.prompt())
            return response
        except TypeError:
            async def error_coro():
                return "An error occurred while processing your request."
            return await error_coro()


app = App(app_ui, server, debug=True)
