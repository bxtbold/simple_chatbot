import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.router import chatbot_router


try:
    app = FastAPI()
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"]
    )
    app.include_router(chatbot_router)
    uvicorn.run(app, port=9091)
except KeyboardInterrupt as e:
    pass
except Exception as e:
    print(e)
