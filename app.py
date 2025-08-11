from flask import Flask, render_template, request, Response
from prometheus_client import Counter, generate_latest
from src.data_ingestion import DataIngest
from src.rag_chain import RAGChain
from dotenv import load_dotenv
load_dotenv()

RQ = Counter("http_requests", "Total http requests made")
RESULT_COUNT = Counter("Answers_generated", "Number of time the bot answered")

def create_app():
    app = Flask(__name__)

    vstore = DataIngest().ingest(load_existing=True)
    ragchain = RAGChain(vstore).build_chain()

    @app.route("/")
    def index():
        RQ.inc()
        return render_template("index.html")
    
    @app.route("/get", methods=["Post"])
    def get_response():
        
        RESULT_COUNT.inc()
        user_input = request.form["msg"]
        r = ragchain.invoke(
            {"input":user_input},
            config={"configurable":{"session_id":"user-session"}}
        )["answer"]

        return r

    @app.route("/metrics")
    def metrics():
        return Response(generate_latest(), mimetype="text/plain")
    
    return app

if __name__=="__main__":
    app = create_app()
    app.run(host = "0.0.0.0", port=5000, debug=True)