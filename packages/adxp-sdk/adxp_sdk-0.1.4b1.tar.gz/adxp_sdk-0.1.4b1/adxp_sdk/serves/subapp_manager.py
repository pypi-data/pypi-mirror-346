#!/usr/bin/env python
import uvicorn
import os
import yaml
import logging.config
from autologging import logged
from typing import Dict, Any, Iterator, AsyncIterator, Optional, List
from pathlib import Path
from autologging import logged
from fastapi import FastAPI, Request, HTTPException, Form
from fastapi.middleware.cors import CORSMiddleware
from starlette.datastructures import MutableHeaders
from langchain.prompts import ChatPromptTemplate
from langchain_core.messages import HumanMessage
from langchain_core.runnables import RunnableLambda
from langchain_core.runnables.config import RunnableConfig
from langserve import add_routes
from fastapi.responses import HTMLResponse, RedirectResponse
from adxp_sdk.serves.utils import (
    AIPHeaderMiddleware,
    per_req_config_modifier,
    custom_openapi,
    get_login_html_content,
    add_routes_wrapper,
    init_app,
    add_login,
    load_environment,
)
from adxp_sdk.serves.schema import RemoteRunnableRequest
from pydantic import BaseModel, ConfigDict
import importlib.util


def create_redirect_app(local_redirect_uri: str) -> FastAPI:
    app = FastAPI()
    target_redirect_uri = f"/sub{local_redirect_uri}"
    print("target_redirect_uri", target_redirect_uri)

    @app.post("/invoke")
    async def invoke_redirect(
        request: Request,
        body: RemoteRunnableRequest,
    ):
        body = body.input
        return RedirectResponse("/sub/simple/chat", status_code=307)

    @app.post("/batch")
    async def batch_redirect(
        request: Request,
        body: List[RemoteRunnableRequest],
    ):
        body = body.input
        return RedirectResponse(target_redirect_uri, status_code=307)

    @app.post("/stream")
    async def stream_redirect(
        request: Request,
        body: RemoteRunnableRequest,
    ):
        body = body.input
        return RedirectResponse(target_redirect_uri, status_code=307)

    return app


@logged
def add_subapp(app_path: str) -> FastAPI:
    """add subapp to the main app. main app will redirect to the subapp"""
    try:
        module_file, object_name = app_path.split(":")
    except ValueError:
        raise ValueError(
            "router_path 형식이 올바르지 않습니다. 예시: '/path/to/module.py:object_name'"
        )
    module_file = module_file.strip()
    object_name = object_name.strip()
    spec = importlib.util.spec_from_file_location("dynamic_module", module_file)
    if spec is None or spec.loader is None:
        raise ImportError(f"모듈 {module_file}을(를) 찾을 수 없습니다.")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    try:
        app = getattr(module, object_name)
    except AttributeError:
        raise AttributeError(
            f"모듈 {module_file}에 {object_name}이(가) 존재하지 않습니다."
        )
    return app
