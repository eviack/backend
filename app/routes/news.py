from fastapi import APIRouter, HTTPException

from app.models.schema import NewsItem
from app.core.workflow import FactCheckingWorkflowManager

from datetime import datetime

router = APIRouter()

@router.post("/news-check", response_model=NewsItem)
async def fact_check_news(item: NewsItem):
    """
    Accepts a JSON body with a 'input_data' field, processes it using the fact-checking workflow,
    and saves the resulting report in MongoDB.
    """
    try:
        
        workflow_manager = FactCheckingWorkflowManager()
        state = workflow_manager.run_workflow(item.input_data)
        
        final_state = {
            "report":state['report'],
            "relevant_metadata":state['relevant_metadata'],
            "metadata":state['metadata']
            }
        
        
        return final_state
    except Exception as e:
        raise HTTPException(status_code=500, detail=e)
    
    
