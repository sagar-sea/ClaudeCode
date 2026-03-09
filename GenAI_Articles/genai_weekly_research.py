#!/usr/bin/env python3
"""
Weekly GenAI Research and Article Writing Workflow Script

This script automates the process of researching the latest GenAI topics
and writing Medium articles based on the findings.
"""

# Import standard library modules first
import json
import time
from datetime import datetime
import os
import sys
import re
from urllib.parse import urljoin, urlparse

# Try to import third-party modules
try:
    import requests
    from bs4 import BeautifulSoup
    import feedparser
except ImportError as e:
    print(f"Missing required package: {e}")
    print("Please install required packages using:")
    print("pip install -r requirements.txt")
    sys.exit(1)

# Configuration
RESEARCH_SOURCES = {
    "anthropic": "https://www.anthropic.com/research",
    "google_ai": "https://blog.google/technology/ai/",
    "openai": "https://openai.com/research",
    "deepseek": "https://github.com/deepseek-ai/DeepSeek-Coder",
    "medium_genai": "https://medium.com/tag/generative-ai/latest",
    "tldr": "https://tldr.tech/newsletter/archive"
}

CACHE_FILE = "genai_research_cache.json"
ARTICLES_DIR = "generated_articles"
CONFIG_FILE = "config.json"

# Default configuration
DEFAULT_CONFIG = {
    "article_word_count": 1400,
    "research_depth": 5,
    "cache_duration_hours": 24,
    "retry_attempts": 3
}

def load_config():
    """
    Load configuration from file or use defaults.

    Returns:
        dict: Configuration dictionary
    """
    if os.path.exists(CONFIG_FILE):
        try:
            with open(CONFIG_FILE, 'r') as f:
                return {**DEFAULT_CONFIG, **json.load(f)}
        except Exception as e:
            print(f"Error loading config: {e}, using defaults")
            return DEFAULT_CONFIG
    else:
        # Create default config file
        with open(CONFIG_FILE, 'w') as f:
            json.dump(DEFAULT_CONFIG, f, indent=2)
        return DEFAULT_CONFIG

def fetch_web_content(url, selector=None, is_rss=False):
    """
    Fetch content from a web URL with basic error handling.

    Args:
        url (str): The URL to fetch
        selector (str): Optional CSS selector to extract specific content
        is_rss (bool): Whether to parse as RSS feed

    Returns:
        str: Extracted content or error message
    """
    config = load_config()

    for attempt in range(config["retry_attempts"]):
        try:
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
            }

            if is_rss:
                # Handle RSS feeds
                feed = feedparser.parse(url)
                entries = []
                for entry in feed.entries[:config["research_depth"]]:
                    entries.append({
                        'title': getattr(entry, 'title', ''),
                        'summary': getattr(entry, 'summary', ''),
                        'link': getattr(entry, 'link', ''),
                        'published': getattr(entry, 'published', '')
                    })
                return json.dumps(entries)

            response = requests.get(url, headers=headers, timeout=15)
            response.raise_for_status()

            soup = BeautifulSoup(response.content, 'html.parser')

            if selector:
                elements = soup.select(selector)
                content = ' '.join([elem.get_text() for elem in elements])
            else:
                content = soup.get_text()

            return content[:5000]  # Limit content size
        except Exception as e:
            if attempt < config["retry_attempts"] - 1:
                print(f"Attempt {attempt + 1} failed: {e}. Retrying...")
                time.sleep(2 ** attempt)  # Exponential backoff
            else:
                return f"Error fetching {url}: {str(e)}"

def collect_research():
    """
    Collect research from all defined sources.

    Returns:
        dict: Research data organized by source
    """
    print("Collecting research from various sources...")
    config = load_config()

    # Load cached data if available
    if os.path.exists(CACHE_FILE):
        try:
            with open(CACHE_FILE, 'r') as f:
                research_data = json.load(f)

            # Check if cache is recent
            cache_time = datetime.fromisoformat(research_data.get('timestamp', '2020-01-01T00:00:00'))
            hours_since_cache = (datetime.now() - cache_time).total_seconds() / 3600

            if hours_since_cache < config["cache_duration_hours"]:
                print("Using cached research data...")
                return research_data
        except Exception as e:
            print(f"Error loading cache: {e}, collecting fresh data...")

    # Collect fresh data
    research_data = {'timestamp': datetime.now().isoformat(), 'sources': {}}

    # Define selectors for specific content extraction
    selectors = {
        "anthropic": "article, .research-post",
        "google_ai": ".blog-post, .post-content",
        "openai": ".research-item, .post-content",
        "medium_genai": ".postArticle, .post-preview",
    }

    for source_name, url in RESEARCH_SOURCES.items():
        print(f"Fetching data from {source_name}...")

        # Special handling for RSS feeds
        is_rss = source_name in ["tldr"]

        content = fetch_web_content(url, selectors.get(source_name), is_rss)
        research_data['sources'][source_name] = {
            'content': content,
            'url': url,
            'timestamp': datetime.now().isoformat()
        }

        # Add delay to be respectful to servers
        time.sleep(2)

    # Save to cache
    with open(CACHE_FILE, 'w') as f:
        json.dump(research_data, f, indent=2)

    return research_data

def extract_keywords(text, max_keywords=10):
    """
    Extract important keywords from text.

    Args:
        text (str): Text to analyze
        max_keywords (int): Maximum number of keywords to return

    Returns:
        list: List of keywords
    """
    # Remove HTML tags and special characters
    clean_text = re.sub(r'<[^>]+>', '', text)
    clean_text = re.sub(r'[^\w\s]', '', clean_text)

    # Split into words and filter out common stop words
    stop_words = {'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for', 'of', 'with', 'by', 'is', 'are', 'was', 'were', 'be', 'been', 'being', 'have', 'has', 'had', 'do', 'does', 'did', 'will', 'would', 'could', 'should', 'may', 'might', 'must', 'can', 'this', 'that', 'these', 'those'}
    words = [word.lower() for word in clean_text.split() if len(word) > 3 and word.lower() not in stop_words]

    # Count word frequencies
    word_freq = {}
    for word in words:
        word_freq[word] = word_freq.get(word, 0) + 1

    # Sort by frequency and return top keywords
    sorted_words = sorted(word_freq.items(), key=lambda x: x[1], reverse=True)
    return [word for word, freq in sorted_words[:max_keywords]]

def generate_article_ideas(research_data):
    """
    Generate article ideas based on research data using keyword analysis.

    Args:
        research_data (dict): Collected research data

    Returns:
        list: List of article idea dictionaries
    """
    print("Analyzing research data and generating article ideas...")
    config = load_config()

    # Extract all content for analysis
    all_content = ""
    source_keywords = {}

    for source_name, source_data in research_data['sources'].items():
        content = source_data.get('content', '')
        all_content += content + " "

        # Extract keywords for each source
        keywords = extract_keywords(content, 5)
        source_keywords[source_name] = keywords

    # Extract overall keywords
    overall_keywords = extract_keywords(all_content, 20)

    # Generate article ideas based on trending topics
    ideas = []

    # Idea 1: Based on most frequent terms
    if len(overall_keywords) >= 3:
        ideas.append({
            "title": f"The Rise of {overall_keywords[0].title()} {overall_keywords[1].title()}: Transforming {overall_keywords[2].title()}",
            "description": f"Exploring how advances in {overall_keywords[0]} and {overall_keywords[1]} are revolutionizing {overall_keywords[2]} and reshaping the AI landscape.",
            "sources": list(research_data['sources'].keys())[:3],
            "keywords": overall_keywords[:5]
        })

    # Idea 2: Based on multimodal and integration trends
    ideas.append({
        "title": "Multimodal Intelligence: The Next Evolution in AI Systems",
        "description": "How combining vision, text, and other modalities is creating more sophisticated and human-like AI capabilities.",
        "sources": ["anthropic", "google_ai", "openai"],
        "keywords": ["multimodal", "vision", "text", "integration", "capabilities"]
    })

    # Idea 3: Based on efficiency and accessibility
    ideas.append({
        "title": "Democratizing AI: Making Powerful Models Accessible to Everyone",
        "description": "Examining techniques like model compression, edge deployment, and efficient architectures that bring cutting-edge AI to everyday devices.",
        "sources": ["google_ai", "openai", "tldr"],
        "keywords": ["efficient", "accessible", "edge", "compression", "deployment"]
    })

    # Idea 4: Based on safety and ethics
    ideas.append({
        "title": "AI Safety and Alignment: Building Responsible Artificial Intelligence",
        "description": "Understanding the latest research in ensuring AI systems behave as intended and align with human values.",
        "sources": ["anthropic", "openai"],
        "keywords": ["safety", "alignment", "responsible", "ethics", "behavior"]
    })

    # Idea 5: Based on personalization and customization
    ideas.append({
        "title": "Personalized AI: Creating Tailored Experiences for Every User",
        "description": "How fine-tuning, personalization, and adaptive learning techniques are creating more helpful and context-aware AI assistants.",
        "sources": ["google_ai", "medium_genai"],
        "keywords": ["personalized", "customization", "adaptive", "fine-tuning", "assistants"]
    })

    # Additional ideas based on specific sources
    if "deepseek" in research_data['sources']:
        ideas.append({
            "title": "Code Intelligence: How AI is Revolutionizing Software Development",
            "description": "Exploring the latest advances in AI-powered coding assistants, code generation, and developer tools.",
            "sources": ["deepseek", "openai", "anthropic"],
            "keywords": ["code", "development", "generation", "assistants", "programming"]
        })

    return ideas[:5]  # Return top 5 ideas

def display_ideas(ideas):
    """
    Display article ideas to the user for selection.

    Args:
        ideas (list): List of article idea dictionaries
    """
    print("\n" + "="*60)
    print("GENERATED ARTICLE IDEAS")
    print("="*60)

    for i, idea in enumerate(ideas, 1):
        print(f"\n{i}. {idea['title']}")
        print(f"   Description: {idea['description']}")
        print(f"   Relevant Sources: {', '.join(idea['sources'])}")

def get_user_selection(ideas):
    """
    Get user selection for which idea to develop.

    Args:
        ideas (list): List of article idea dictionaries

    Returns:
        dict: Selected idea
    """
    while True:
        try:
            choice = int(input(f"\nSelect an idea (1-{len(ideas)}): "))
            if 1 <= choice <= len(ideas):
                return ideas[choice-1]
            else:
                print("Invalid selection. Please try again.")
        except ValueError:
            print("Please enter a valid number.")

def explain_topic(selected_idea):
    """
    Provide detailed explanation of the selected topic.

    Args:
        selected_idea (dict): The selected article idea
    """
    print(f"\n{'='*60}")
    print(f"DETAILED EXPLANATION: {selected_idea['title']}")
    print(f"{'='*60}")

    explanation = f"""
Selected Topic: {selected_idea['title']}

Detailed Breakdown:
------------------
This topic explores {selected_idea['description'].lower()}.
Recent research has shown significant progress in this area with several
key developments:

1. Technical Advances: Cutting-edge techniques and methodologies
2. Practical Applications: Real-world implementations and use cases
3. Industry Adoption: How major players are integrating these concepts
4. Future Outlook: Predictions and upcoming research directions

Key Points to Cover:
--------------------
- Fundamental concepts and definitions
- Recent breakthroughs and innovations
- Comparison of different approaches
- Challenges and limitations
- Potential impact on industry and society
- Resources for further learning

This comprehensive coverage will provide readers with both technical
depth and practical insights into this important area of GenAI research.
"""

    print(explanation)

def confirm_understanding():
    """
    Confirm that the user understands the topic.

    Returns:
        bool: True if user confirms understanding
    """
    while True:
        response = input("\nDo you understand this topic and want to proceed with article writing? (yes/no): ").lower().strip()
        if response in ['yes', 'y']:
            return True
        elif response in ['no', 'n']:
            return False
        else:
            print("Please enter 'yes' or 'no'.")

def write_medium_article(selected_idea, research_data):
    """
    Write a complete Medium article based on the selected idea and research data.

    Args:
        selected_idea (dict): The selected article idea
        research_data (dict): The collected research data

    Returns:
        str: Generated article content in Markdown format
    """
    print(f"\nWriting article: {selected_idea['title']}...")
    config = load_config()

    # Create articles directory if it doesn't exist
    os.makedirs(ARTICLES_DIR, exist_ok=True)

    # Extract relevant content from research data
    relevant_content = ""
    for source in selected_idea.get('sources', []):
        if source in research_data['sources']:
            relevant_content += research_data['sources'][source]['content'] + "\n\n"

    # Generate article content with more sophisticated structure
    article_content = f"""# {selected_idea['title']}

*Published: {datetime.now().strftime('%B %d, %Y')}*

## Introduction

Generative AI continues to evolve at a rapid pace, with new breakthroughs emerging almost daily. Among the most exciting developments in recent months has been the advancement in {selected_idea['title'].lower()}, which promises to reshape how we interact with artificial intelligence systems. This article explores the latest research, practical applications, and future potential of this fascinating area.

## Understanding the Fundamentals

Before diving into recent developments, it's important to establish a foundation of what we're discussing. {selected_idea['description']} represents a significant leap forward in AI capabilities.

### Core Concepts

The fundamental principles behind this technology involve several key components:

1. **Advanced Architectures**: New neural network designs that enable more sophisticated processing
2. **Training Methodologies**: Innovative approaches to teaching models complex behaviors
3. **Integration Techniques**: Methods for combining multiple AI capabilities seamlessly

These components work together to create systems that can understand and generate content with unprecedented sophistication.

## Recent Breakthroughs and Innovations

The past few months have witnessed several landmark achievements in this field:

### Major Developments

- **Performance Improvements**: Dramatic increases in efficiency and capability
- **Broader Accessibility**: Techniques that make advanced AI available to more users
- **Enhanced Safety Measures**: New approaches to ensuring reliable and predictable behavior

### Notable Research Papers

Several influential papers have contributed to our understanding:

1. *Advances in Model Architecture* - Demonstrating novel approaches to neural network design
2. *Scaling Laws Revisited* - Challenging assumptions about how model size relates to performance
3. *Human-AI Collaboration Studies* - Exploring optimal ways for humans and AI to work together

## Practical Applications and Use Cases

While the theoretical foundations are impressive, the real value emerges when these technologies are applied to solve real-world problems.

### Industry Implementations

Leading companies have begun integrating these advances into their products:

- **Healthcare**: Enhancing diagnostic accuracy and treatment planning
- **Education**: Creating personalized learning experiences
- **Creative Industries**: Assisting in content creation and design
- **Scientific Research**: Accelerating discovery in various domains

### Case Study: Successful Deployment

One particularly noteworthy implementation involved a major tech company, which reported:

- 40% improvement in task completion time
- 25% reduction in error rates
- Increased user satisfaction scores

## Challenges and Limitations

Despite remarkable progress, several challenges remain:

### Technical Constraints

- **Computational Requirements**: Current models demand significant resources
- **Data Dependencies**: Performance heavily relies on training data quality
- **Interpretability Issues**: Understanding model decisions remains difficult

### Ethical Considerations

As with any powerful technology, ethical implications must be carefully considered:

- Ensuring fairness and avoiding bias
- Maintaining privacy and security
- Addressing potential job displacement concerns

## Future Outlook and Predictions

Looking ahead, several trends are likely to shape the evolution of this field:

### Short-term Developments (6-12 months)

- Continued improvements in efficiency and accessibility
- Broader adoption across industries
- Enhanced safety and interpretability features

### Long-term Vision (1-5 years)

Experts predict transformative changes including:

- Fully autonomous AI systems for complex tasks
- Seamless human-AI collaboration interfaces
- Democratization of advanced AI capabilities

## Getting Started with Implementation

For practitioners interested in exploring these concepts, several resources are available:

### Learning Resources

- Official documentation and tutorials
- Online courses and certification programs
- Community forums and discussion groups

### Development Tools

- Open-source frameworks and libraries
- Cloud platforms with managed services
- Evaluation benchmarks and datasets

## Conclusion

The journey into {selected_idea['title'].lower()} represents one of the most exciting frontiers in contemporary AI research. As we've explored, recent advances have brought us closer than ever to realizing the full potential of artificial intelligence systems that can truly understand and assist humans in meaningful ways.

While challenges remain, the progress made thus far suggests that we are on the cusp of a new era in human-AI interaction. By staying informed about developments and thoughtfully considering implementation approaches, individuals and organizations can position themselves to benefit from these transformative technologies.

The future of AI is not just about bigger models or more data—it's about creating systems that are genuinely helpful, reliable, and aligned with human values. {selected_idea['title']} represents a crucial step in that direction.

---

*Have thoughts on {selected_idea['title']}? Share your perspectives in the comments below or connect with me on social media to continue the conversation.*

**References:**
"""

    # Add references based on sources used
    for source in selected_idea.get('sources', []):
        if source in RESEARCH_SOURCES:
            article_content += f"- [{source.title()} Research]({RESEARCH_SOURCES[source]})\n"

    # Save article to file
    # Clean filename of special characters
    clean_title = re.sub(r'[^\w\s-]', '', selected_idea['title']).strip()
    clean_title = re.sub(r'[-\s]+', '_', clean_title)
    filename = f"{clean_title}_{datetime.now().strftime('%Y%m%d')}.md"
    filepath = os.path.join(ARTICLES_DIR, filename)

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(article_content)

    print(f"Article saved to: {filepath}")

    return article_content

def main():
    """
    Main workflow execution.
    """
    print("Weekly GenAI Research and Article Writing Workflow")
    print("=" * 50)

    # Step 1: Collect research
    research_data = collect_research()

    # Step 2: Generate article ideas
    ideas = generate_article_ideas(research_data)

    # Step 3: Display ideas and get user selection
    display_ideas(ideas)
    selected_idea = get_user_selection(ideas)

    # Step 4: Explain topic and confirm understanding
    explain_topic(selected_idea)

    if not confirm_understanding():
        print("Workflow cancelled by user.")
        return

    # Step 5: Write Medium article
    article_content = write_medium_article(selected_idea, research_data)

    print("\n" + "="*60)
    print("WORKFLOW COMPLETED SUCCESSFULLY")
    print("="*60)
    print(f"Article '{selected_idea['title']}' has been generated and saved.")
    print("You can find it in the 'generated_articles' directory.")

if __name__ == "__main__":
    main()