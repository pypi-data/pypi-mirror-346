from mock.mock_app.handlers.routers import work_router

from argenta.app import App
from argenta.app.defaults import PredefinedMessages
from argenta.app.autocompleter import AutoCompleter
from argenta.orchestrator import Orchestrator
from argenta.orchestrator.argparser import ArgParser
from argenta.orchestrator.argparser.arguments import BooleanArgument


arg_parser = ArgParser(processed_args=[BooleanArgument('repeat')])
app: App = App(autocompleter=AutoCompleter('.hist'))
orchestrator: Orchestrator = Orchestrator()


def main():
    app.include_router(work_router)

    app.add_message_on_startup(PredefinedMessages.USAGE)
    app.add_message_on_startup(PredefinedMessages.AUTOCOMPLETE)
    app.add_message_on_startup(PredefinedMessages.HELP)

    orchestrator.start_polling(app)

if __name__ == "__main__":
    main()
