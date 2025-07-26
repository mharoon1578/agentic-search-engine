import streamlit as st
from langchain_groq import ChatGroq
from langchain_community.utilities import ArxivAPIWrapper, WikipediaAPIWrapper
from langchain_community.tools import ArxivQueryRun, WikipediaQueryRun, DuckDuckGoSearchRun
from langchain.agents import initialize_agent, AgentType
from langchain.callbacks import StreamlitCallbackHandler
from langchain.memory import ConversationBufferMemory
from langchain.tools import Tool
from duckduckgo_search import DDGS
import re

# Page config
st.set_page_config(page_title="Agentic Research Engine", layout="wide")

# Tools setup
arxiv = ArxivQueryRun(api_wrapper=ArxivAPIWrapper(top_k_results=1, doc_content_chars_max=200))
wiki = WikipediaQueryRun(api_wrapper=WikipediaAPIWrapper(top_k_results=1, doc_content_chars_max=200))
search = DuckDuckGoSearchRun(name="Search")

def duckduckgo_image_search(query: str) -> list[str]:
    try:
        with DDGS() as ddgs:
            results = ddgs.images(query, max_results=6)
            urls = [r["image"] for r in results if "image" in r]
        return urls
    except Exception as e:
        st.error(f"Image search error: {e}")
        return []

def image_search_wrapper(query: str) -> str:
    urls = duckduckgo_image_search(query)
    if not urls:
        return "No images found for the query."
  
    result = f"Found {len(urls)} images for '{query}':\n"
    for i, url in enumerate(urls, 1):
        result += f"Image {i}: {url}\n"
    
    return result

image_search_tool = Tool(
    name="ImageSearch",
    func=image_search_wrapper,
    description="Searches for and returns image URLs related to the query. Use this when the user asks for images or visual content."
)

# Function to extract image URLs from text
def extract_image_urls(text):
    url_pattern = r'https?://[^\s]+'
    urls = re.findall(url_pattern, text)
    image_urls = []
    for url in urls:
        url = url.rstrip('.,;!?')
        image_urls.append(url)
    
    return image_urls

# Function to check if response contains mainly image URLs
def is_image_response(text):
    text_lower = text.lower()
    image_patterns = [
        'here are some images',
        'image 1:',
        'image 2:',
        'image 3:',
        'found for you:'
    ]
    
    # Check if any image patterns are found
    has_image_patterns = any(pattern in text_lower for pattern in image_patterns)
    
    # Check for image file extensions in URLs
    has_image_urls = 'https://' in text and any(ext in text_lower for ext in ['.jpg', '.jpeg', '.png', '.gif', '.webp'])
    
    # Count URLs in the response
    url_count = len(re.findall(r'https?://[^\s]+', text))
    
    return has_image_patterns or has_image_urls or url_count >= 3

# App UI and sidebar
st.title("🔎 Agentic Search Chat")
st.sidebar.title("⚙️ Settings")
api_key = st.sidebar.text_input("Enter your Groq API Key:", type="password")

if not api_key:
    st.warning("Please provide your Groq API key to start.")
    st.stop()

if "memory" not in st.session_state:
    st.session_state.memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)

if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "Hi! I can research topics, fetch summaries, and show images. Try asking for images by saying 'show me images of...' or 'find pictures of...'"}
    ]


for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])
    
    # Display images if the message contains image URLs
    if msg["role"] == "assistant" and "image_urls" in msg:
        cols = st.columns(3)
        for i, url in enumerate(msg["image_urls"]):
            with cols[i % 3]:
                try:
                    st.image(url, caption=f"Image {i+1}", use_container_width=True)
                except:
                    st.write(f"Could not load: Image {i+1}")

# Handle user queries
if prompt := st.chat_input("Ask your research question..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.chat_message("user").write(prompt)

    llm = ChatGroq(groq_api_key=api_key, model_name="llama3-70b-8192")
    tools = [search, arxiv, wiki, image_search_tool]
  
    system_prompt = """You are a helpful research assistant. When users ask for images, pictures, or visual content, use the ImageSearch tool. 
    For other queries, use the appropriate tools (Search, ArxivQueryRun, WikipediaQueryRun).
    Be concise and informative in your responses."""

    agent = initialize_agent(
        tools=tools,
        llm=llm,
        agent=AgentType.CONVERSATIONAL_REACT_DESCRIPTION,
        memory=st.session_state.memory,
        handle_parsing_errors=True,
        verbose=False,
    )

    with st.chat_message("assistant"):
        st_cb = StreamlitCallbackHandler(st.container(), expand_new_thoughts=False)
        
        try:
            response = agent.run(prompt, callbacks=[st_cb])
            
            if is_image_response(response):
                image_urls = extract_image_urls(response)
                
                if image_urls:
                    st.write("🖼️ Here are the images I found:")
                    
                    cols = st.columns(3) 
                    for i, url in enumerate(image_urls[:6]): 
                        with cols[i % 3]:
                            try:
                                st.image(url, caption=f"Image {i+1}", use_container_width=True)
                            except Exception as e:
                                st.write(f"⚠️ Could not load image {i+1}: {url}")
                    
                    # Store image URLs in session state for chat history
                    message_with_images = {
                        "role": "assistant", 
                        "content": f"Found {len(image_urls)} images for your search.",
                        "image_urls": image_urls
                    }
                    st.session_state.messages.append(message_with_images)
                else:
                    st.write(response)
                    st.session_state.messages.append({"role": "assistant", "content": response})
            else:
                st.write(response)
                st.session_state.messages.append({"role": "assistant", "content": response})
                
        except Exception as e:
            error_msg = f"An error occurred: {str(e)}"
            st.error(error_msg)
            st.session_state.messages.append({"role": "assistant", "content": error_msg})


st.sidebar.markdown("### 💡 Example Queries")
st.sidebar.markdown("""
**For Images:**
- "Show me images of cats"
- "Find pictures of the Eiffel Tower"
- "Images of quantum computing"

**For Research:**
- "What is machine learning?"
- "Latest research on AI"
- "Tell me about quantum physics"
""")

# Add clear chat button
if st.sidebar.button("🗑️ Clear Chat History"):
    st.session_state.messages = [
        {"role": "assistant", "content": "Hi! I can research topics, fetch summaries, and show images. Try asking for images by saying 'show me images of...' or 'find pictures of...'"}
    ]
    st.session_state.memory.clear()
    st.rerun()
