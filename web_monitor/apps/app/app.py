# -*- coding:utf-8 -*-

import turbo.log

from .base import BaseHandler

logger = turbo.log.getLogger(__file__)


class HomeHandler(BaseHandler):

    def get(self):
        self.render('index.html')
