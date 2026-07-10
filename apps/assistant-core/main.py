"""
main.py

Bootstrap entry point.
"""

from app.config.config_loader import ConfigLoader
from app.config.settings import Settings

from app.core.assistant_engine import AssistantEngine
from app.core.command_dispatcher import CommandDispatcher
from app.core.conversation_manager import ConversationManager
from app.core.plugin_manager import PluginManager
from app.core.plugin_registry import PluginRegistry
from app.core.response_engine import ResponseEngine

from app.logging.logger_service import LoggerService

from app.providers.mock_llm_provider import MockLLMProvider

from app.services.capability_context_builder import CapabilityContextBuilder
from app.services.intent_parser import IntentParser
from app.services.process_service import ProcessService
from app.services.resource_registry import ResourceRegistry

from plugins.application.application_plugin import ApplicationPlugin
from plugins.browser.browser_plugin import BrowserPlugin


def main() -> None:

    # ---------------------------------------------------------
    # Configuration
    # ---------------------------------------------------------

    settings = ConfigLoader(Settings()).load()
    logger = LoggerService(settings.log_directory)
    logger.info("Assistant starting...")

    # ---------------------------------------------------------
    # Core services
    # ---------------------------------------------------------

    plugin_registry = PluginRegistry()
    plugin_manager = PluginManager(
        registry=plugin_registry,
        logger=logger,
    )

    resource_registry = ResourceRegistry()

    # ---------------------------------------------------------
    # Plugin registration
    # ---------------------------------------------------------

    process_service = ProcessService()

    plugin_manager.load_plugin(ApplicationPlugin(registry=resource_registry, process_service=process_service,))
    plugin_manager.load_plugin(BrowserPlugin(registry=resource_registry, process_service=process_service,))

    logger.info("Registered plugins", count=len(plugin_registry.plugins),)
    logger.info("Registered capabilities", capabilities=list(plugin_registry.capabilities),)

    # ---------------------------------------------------------
    # Assistant pipeline
    # ---------------------------------------------------------

    dispatcher = CommandDispatcher(plugin_registry)
    
    context_builder = CapabilityContextBuilder(plugin_registry=plugin_registry, resource_registry=resource_registry,)
    intent_parser = IntentParser(resource_registry=resource_registry,)

    llm = MockLLMProvider(capability_context=context_builder.build(), parser=intent_parser,)
    response_engine = ResponseEngine(llm_provider=llm,)

    conversation_manager = ConversationManager()

    assistant = AssistantEngine(
        llm=llm, dispatcher=dispatcher,
        response_engine=response_engine, conversation_manager=conversation_manager,
        logger=logger,
    )

    logger.info("Assistant Ready.")

    # ---------------------------------------------------------
    # CLI loop
    # ---------------------------------------------------------

    while True:

        command = input("> ").strip()

        if not command:
            continue

        if command.lower() == "exit":
            break

        response = assistant.process(command)
        print(response)


if __name__ == "__main__":
    main()








# """
# main.py

# Bootstrap entry point.
# """

# from app.config.config_loader import ConfigLoader
# from app.config.settings import Settings
# from app.core.conversation_manager import ConversationManager
# from app.core.response_engine import ResponseEngine
# from app.core.assistant_engine import AssistantEngine
# from app.core.command_dispatcher import CommandDispatcher
# from app.core.plugin_manager import PluginManager
# from app.core.plugin_registry import PluginRegistry
# from app.providers.mock_llm_provider import MockLLMProvider
# from app.logging.logger_service import LoggerService
# from app.services.resource_registry import ResourceRegistry


# def main() -> None:

#     settings = Settings()
#     settings = ConfigLoader(settings).load()

#     logger = LoggerService(settings.log_directory)
#     logger.info("Assistant starting...")

#     registry = PluginRegistry()
#     manager = PluginManager(
#         registry=registry,
#         logger=logger,
#     )
    
#     resource_registry = ResourceRegistry()
#     manager.load_plugin()
    
#     dispatcher = CommandDispatcher(registry)
#     llm = MockLLMProvider()

#     logger.info("Plugin Manager initialized.")
#     logger.info("Assistant Ready.")
    
#     response_engine = ResponseEngine(llm_provider=llm)
#     conversation_manager = ConversationManager()
    
    
#     # while True:

#     #     user = input("> ")
#     #     intent, response = llm.parse_intent(user)
#     #     print(intent.capability)
#     #     print(response)
#     #     print(dispatcher.dispatch(intent))
    
#     assistant = AssistantEngine(
#         llm=llm,
#         dispatcher=dispatcher,
#         response_engine=response_engine,
#         conversation_manager=conversation_manager,
#         logger=logger,
#     )

#     while True:
#         command = input("> ")

#         if command.lower() == "exit":
#             break

#         response = assistant.process(command)

#         print(response.assistant_message)
        
    

# if __name__ == "__main__":
#     main()
