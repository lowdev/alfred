import pkgutil
import os
import logging

class Actions:
    TOP_DIR = os.path.dirname(os.path.abspath(__file__))
    MODULE_PATH = os.path.join(TOP_DIR, "module")

    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.modules = self.__initModules() 

    def __initModules(self):
        modules = []

        for finder, name, ispkg in pkgutil.walk_packages([self.MODULE_PATH]):
            try:
                loader = finder.find_module(name)
                mod = loader.load_module(name)
            except:
                self.logger.warning("Skipped module '%s' due to an error.", name,
                               exc_info=True)
            else:
                if hasattr(mod, 'WORDS'):
                    self.logger.debug("Found module '%s' with words: %r", name,
                                 mod.WORDS)
                    modules.append(mod)
                else:
                    self.logger.warning("Skipped module '%s' because it misses " +
                                   "the WORDS constant.", name)
        modules.sort(key=lambda mod: mod.PRIORITY if hasattr(mod, 'PRIORITY')
                     else 0, reverse=True)

        return modules  

    def execute(self, text):
        for module in self.modules:
            if module.isValid(text):
                self.logger.debug("'%s' is a valid phrase for module " +
                                       "'%s'", text, module.__name__)
                action = ''
                try:
                    action =  module.handle(text)
                except Exception:
                    self.logger.error('Failed to execute module',
                                       exc_info=True)
                else:
                    self.logger.debug("Handling of phrase '%s' by " +
                                       "module '%s' completed", text,
                                       module.__name__)
                finally:
                    return action
        
        self.logger.debug("No module was able to handle any of these " +
                           "phrases: %r", texts)
