from starlette.middleware.base import BaseHTTPMiddleware
from fastapi import Request
from fastapi.responses import JSONResponse
from utils.feature_extractor import FeatureExtractor
import pandas as pd
from ml_model import MODEL  # اگر میخوای مدل را همینجا استفاده کنی


class FeatureExtractionMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        headers = dict(request.headers)
        method = request.method
        url = str(request.url)
        body_bytes = await request.body()
        body = body_bytes.decode("utf-8") if body_bytes else ""

        # استخراج فیچرها
        extractor = FeatureExtractor(headers, method, url, body)
        features = extractor.extract()
        request.state.features = features

        # تبدیل به DataFrame برای مدل
        df = pd.DataFrame([features])

        print(df)
        prediction = MODEL.predict(df)[0]  # خروجی مدل، فرض کنیم 0 یا 1

        # تصمیم gateway
        if prediction == 1:
            return JSONResponse({"detail": "Request blocked by ML model"}, status_code=403)

        # ادامه مسیر به endpoint
        response = await call_next(request)
        return response
