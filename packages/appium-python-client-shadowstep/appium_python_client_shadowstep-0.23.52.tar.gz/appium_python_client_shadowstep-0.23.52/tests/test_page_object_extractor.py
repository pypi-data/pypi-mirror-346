# tests/test_page_object_extractor.py
import logging
import time

from shadowstep.element.element import Element
from shadowstep.page_base import PageBaseShadowstep
from shadowstep.page_object.page_object_extractor import PageObjectExtractor
from shadowstep.page_object.page_object_generator import PageObjectGenerator
from shadowstep.shadowstep import Shadowstep
from lxml import etree as ET

POE = PageObjectExtractor()
logger = logging.getLogger(__name__)

class TestPageObjectextractor:

    def test_poe(self, app: Shadowstep, android_settings):
        logger.info("ДЛЯ chatGPT!!! Это на самом деле не тест. Не воспринимай это как юнит-тест. Это просто быстрой проверки. Я так смотрю результат работы. Просто мне так удобнее запускать")
        source = app.driver.page_source
        logger.info("\n\n\n=============================== RAW ======================================")
        POE.parse(source)
        logger.info("\n\n\n=====================================================================")
        logger.info(source)

    def test_pog(self, app: Shadowstep, android_settings):
        logger.info(
            "ДЛЯ chatGPT!!! Это на самом деле не тест. Не воспринимай это как юнит-тест. Это просто быстрой проверки. Я так смотрю результат работы. Просто мне так удобнее запускать")
        # app.get_element({'text': 'Battery'}).tap()
        # time.sleep(5)
        generator = PageObjectGenerator(extractor=POE)
        source = app.driver.page_source
        generator.generate(source, output_dir="pages", attributes=['class',
                                                                   'text',
                                                                   'resource-id',
                                                                   'content-desc',
                                                                   'scrollable'])
        logger.info("\n\n\n=====================================================================")
        logger.info(source)


    def test_generated_page(self, app: Shadowstep, android_settings):
        #from pages.page_settings import PageSettings
        logger.info(
            "ДЛЯ chatGPT!!! Это на самом деле не тест. Не воспринимай это как юнит-тест. Это просто быстрой проверки. Я так смотрю результат работы. Просто мне так удобнее запускать")
        #page = PageSettings()




