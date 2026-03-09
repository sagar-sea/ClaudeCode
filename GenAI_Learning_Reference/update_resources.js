const fs = require('fs');
const path = require('path');

const filePath = path.join(__dirname, 'index.html');
let html = fs.readFileSync(filePath, 'utf8');

const resourcesMap = {
    1: [{title: "IBM: What is AI?", url: "https://www.ibm.com/topics/artificial-intelligence"}, {title: "Coursera: AI For Everyone", url: "https://www.coursera.org/learn/ai-for-everyone"}],
    2: [{title: "NVIDIA: What are Large Language Models?", url: "https://www.nvidia.com/en-us/glossary/data-science/large-language-models/"}, {title: "AWS: What is an LLM?", url: "https://aws.amazon.com/what-is/large-language-model/"}],
    3: [{title: "Hugging Face: NLP Course", url: "https://huggingface.co/learn/nlp-course"}, {title: "KDNuggets: Hyperparameter Tuning", url: "https://www.kdnuggets.com/2021/01/hyperparameter-tuning-machine-learning.html"}],
    4: [{title: "OpenAI: Prompt Engineering Guide", url: "https://platform.openai.com/docs/guides/prompt-engineering"}, {title: "Anthropic: Prompt Engineering", url: "https://docs.anthropic.com/en/docs/build-with-claude/prompt-engineering/overview"}],
    5: [{title: "Model Context Protocol Official Site", url: "https://modelcontextprotocol.io/"}, {title: "Anthropic: MCP Intro", url: "https://www.anthropic.com/news/model-context-protocol"}],
    6: [{title: "LangChain: Tools", url: "https://js.langchain.com/docs/concepts/tools/"}, {title: "OpenAI: Function Calling", url: "https://platform.openai.com/docs/guides/function-calling"}],
    7: [{title: "OpenAI Tokenizer", url: "https://platform.openai.com/tokenizer"}, {title: "Anthropic: Glossary - Token", url: "https://docs.anthropic.com/en/docs/resources/glossary#token"}],
    8: [{title: "OpenAI: Fine-tuning", url: "https://platform.openai.com/docs/guides/fine-tuning"}, {title: "Hugging Face: Fine-tuning Transformers", url: "https://huggingface.co/docs/transformers/training"}],
    9: [{title: "IBM: What is Retrieval-Augmented Generation?", url: "https://www.ibm.com/topics/retrieval-augmented-generation"}, {title: "Pinecone: RAG Explained", url: "https://www.pinecone.io/learn/retrieval-augmented-generation/"}],
    10: [{title: "Hugging Face: Zero-shot Classification", url: "https://huggingface.co/tasks/zero-shot-classification"}, {title: "IBM: What is Zero-shot learning?", url: "https://www.ibm.com/topics/zero-shot-learning"}],
    11: [{title: "IBM: What is Few-shot learning?", url: "https://www.ibm.com/topics/few-shot-learning"}, {title: "PromptingGuide: Few-Shot Prompting", url: "https://www.promptingguide.ai/techniques/fewshot"}],
    12: [{title: "IBM: What are AI Hallucinations?", url: "https://www.ibm.com/topics/ai-hallucinations"}, {title: "Google Cloud: AI Hallucinations", url: "https://cloud.google.com/discover/what-are-ai-hallucinations"}],
    13: [{title: "Illustrated Transformer by Jay Alammar", url: "https://jalammar.github.io/illustrated-transformer/"}, {title: "Attention Is All You Need (Paper)", url: "https://arxiv.org/abs/1706.03762"}],
    14: [{title: "Cohere: Temperature", url: "https://docs.cohere.com/docs/temperature"}, {title: "OpenAI API Reference", url: "https://platform.openai.com/docs/api-reference"}],
    15: [{title: "Ollama Official Website", url: "https://ollama.com/"}, {title: "Ollama GitHub", url: "https://github.com/ollama/ollama"}],
    16: [{title: "Anthropic: Long Context Window tips", url: "https://docs.anthropic.com/en/docs/build-with-claude/prompt-engineering/long-context-tips"}, {title: "Google Cloud: Context window", url: "https://cloud.google.com/vertex-ai/docs/generative-ai/learn/context-window"}],
    17: [{title: "Pinecone: Vector Embeddings Explained", url: "https://www.pinecone.io/learn/vector-embeddings/"}, {title: "OpenAI: Embeddings", url: "https://platform.openai.com/docs/guides/embeddings"}],
    18: [{title: "LLM Powered Autonomous Agents", url: "https://lilianweng.github.io/posts/2023-06-23-agent/"}, {title: "LangChain: Agents", url: "https://python.langchain.com/docs/concepts/agents/"}],
    19: [{title: "Hugging Face: Diffusion Models Course", url: "https://huggingface.co/course/chapter1/1"}, {title: "NVIDIA: Diffusion Models", url: "https://www.nvidia.com/en-us/glossary/data-science/diffusion-models/"}],
    20: [{title: "Google Cloud: GenAI Path", url: "https://cloud.google.com/training/generative-ai"}, {title: "IBM: Generative AI", url: "https://www.ibm.com/topics/generative-ai"}],
    21: [{title: "IBM: What is a Neural Network?", url: "https://www.ibm.com/topics/neural-networks"}, {title: "3Blue1Brown: Neural Networks", url: "https://www.3blue1brown.com/topics/neural-networks"}],
    22: [{title: "DeepLearning.AI", url: "https://www.deeplearning.ai/"}, {title: "IBM: What is Deep Learning?", url: "https://www.ibm.com/topics/deep-learning"}],
    23: [{title: "Anthropic: System Prompts", url: "https://docs.anthropic.com/en/docs/build-with-claude/prompt-engineering/system-prompts"}, {title: "PromptingGuide: System Prompt", url: "https://www.promptingguide.ai/"}],
    24: [{title: "PromptingGuide: Chain of Thought", url: "https://www.promptingguide.ai/techniques/cot"}, {title: "Chain-of-Thought Paper", url: "https://arxiv.org/abs/2201.11903"}],
    25: [{title: "Cloudflare: AI inference", url: "https://www.cloudflare.com/learning/ai/what-is-ai-inference/"}, {title: "AWS: ML Inference", url: "https://aws.amazon.com/machine-learning/inference/"}],
    26: [{title: "IBM: What is Overfitting?", url: "https://www.ibm.com/topics/overfitting"}, {title: "AWS: Overfitting", url: "https://aws.amazon.com/what-is/overfitting/"}]
};

const match = html.match(/const concepts = \[[\s\S]*?\];/);
if (match) {
    let conceptsStr = match[0];
    let evalStr = conceptsStr.replace('const concepts = ', '');
    const concepts = eval(evalStr);
    
    concepts.forEach(c => {
        c.resources = resourcesMap[c.id] || [];
    });
    
    const newConceptsStr = 'const concepts = ' + JSON.stringify(concepts, null, 16).replace(/\"([a-zA-Z_]+)\":/g, "$1:") + ';';
    html = html.replace(conceptsStr, newConceptsStr);
}

// Update the buttons
html = html.replace('<button class="tab-btn" data-tab="examples">Examples</button>', 
    '<button class="tab-btn" data-tab="examples">Examples</button>\n                        <button class="tab-btn" data-tab="resources">Resources</button>'
);

// Update HTML template
const oldHtmlSection = `<div class="tab-content" data-tab="examples">
                        <div class="description-box">
                            <ul class="examples-list">
                                \${concept.examples.map(example => \`<li>\${example}</li>\`).join('')}
                            </ul>
                        </div>
                    </div>`;

const newHtmlSection = `<div class="tab-content" data-tab="examples">
                        <div class="description-box">
                            <ul class="examples-list">
                                \${concept.examples.map(example => \`<li>\${example}</li>\`).join('')}
                            </ul>
                        </div>
                    </div>
                    
                    <div class="tab-content" data-tab="resources">
                        <div class="description-box">
                            <ul class="examples-list">
                                \${(concept.resources || []).map(r => \`<li><a href="\${r.url}" target="_blank" style="color: #667eea; text-decoration: none; font-weight: 500;">\${r.title} ↗</a></li>\`).join('')}
                            </ul>
                        </div>
                    </div>`;

html = html.replace(oldHtmlSection, newHtmlSection);

// Update CSS rules safely for hyperlinks
if (!html.includes('a:hover')) {
    html = html.replace('</style>', `
        a:hover {
            color: #764ba2 !important;
            text-decoration: underline !important;
        }
    </style>`);
}

fs.writeFileSync(filePath, html);
console.log('Successfully updated index.html');
