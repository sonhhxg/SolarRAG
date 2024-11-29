#!/usr/bin/env python
# -*- coding:utf-8
import uvicorn
from solargs._private.config import Config
CFG = Config()

if __name__=='__main__':
    uvicorn.run("solargs.api.solargs_server:app", host=CFG.HOST, port=CFG.HTTP_PORT, reload=False, workers=CFG.WORKERS)














