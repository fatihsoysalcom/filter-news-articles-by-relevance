import random
import re

def generate_mock_articles(count=50):
    """Generates a list of mock articles with varying relevance."""
    article_templates = [
        {"title": "NVIDIA Unveils New AI GPU for Data Centers", "content": "NVIDIA announced its latest AI GPU, designed to accelerate complex computations in data centers. This new chip features enhanced Tensor Cores and improved CUDA architecture."},
        {"title": "Global Stock Markets React to Economic Data", "content": "Stock markets worldwide saw mixed reactions today following the release of new economic indicators. Technology stocks showed resilience."},
        {"title": "New Software Update Improves System Performance", "content": "A major software update has been released, promising significant improvements in system performance and security. Users are encouraged to install it."},
        {"title": "NVIDIA's Q3 Earnings Exceed Expectations", "content": "NVIDIA reported strong third-quarter earnings, driven by robust demand for its AI and gaming GPUs. The company's data center segment showed exceptional growth."},
        {"title": "Exploring the Future of Autonomous Driving", "content": "Autonomous driving technology continues to advance, with several companies showcasing new prototypes. AI plays a crucial role in these developments."},
        {"title": "Cooking Delicious Pasta Recipes at Home", "content": "Learn how to prepare authentic Italian pasta dishes with simple ingredients. A guide for home cooks."},
        {"title": "AMD Launches Rival GPU Series", "content": "AMD introduced its new line of graphics processing units, aiming to compete in the high-performance computing market. This could impact NVIDIA's market share."},
        {"title": "NVIDIA CUDA Toolkit 13 Released with New Features", "content": "The latest version of the NVIDIA CUDA Toolkit, version 13, is now available, bringing new features for developers working on parallel computing and AI applications."},
        {"title": "Cybersecurity Threats on the Rise", "content": "Experts warn about increasing cybersecurity threats targeting businesses and individuals. Robust protection measures are essential."},
        {"title": "Metaverse Development Gains Momentum", "content": "Investment in metaverse technologies is growing, with companies like NVIDIA providing the foundational GPU infrastructure for virtual worlds."},
        {"title": "Intel's New Processor Architecture Revealed", "content": "Intel unveiled details about its next-generation processor architecture, focusing on efficiency and multi-core performance."},
        {"title": "NVIDIA's Role in Scientific Research", "content": "NVIDIA GPUs are being used in groundbreaking scientific research, from drug discovery to climate modeling, leveraging their parallel processing capabilities."},
        {"title": "Gaming Industry Trends for 2024", "content": "The gaming industry is evolving rapidly, with cloud gaming and advanced graphics (often powered by NVIDIA) shaping future experiences."},
        {"title": "General Tech News: Smartphone Sales Decline", "content": "Reports indicate a decline in global smartphone sales for the past quarter, reflecting broader economic challenges."},
        {"title": "NVIDIA DRIVE Platform Powers Next-Gen Vehicles", "content": "The NVIDIA DRIVE platform is at the forefront of autonomous vehicle development, providing AI computing power for self-driving cars."},
        {"title": "Renewable Energy Investments Surge", "content": "Global investments in renewable energy sources have reached record highs, signaling a shift towards sustainable power."},
        {"title": "AI Ethics and Governance Discussions", "content": "Discussions around AI ethics and governance are becoming more prominent as artificial intelligence integrates deeper into society."},
        {"title": "NVIDIA DGX Systems for Enterprise AI", "content": "NVIDIA DGX systems offer powerful solutions for enterprise AI, enabling companies to deploy large-scale machine learning models."},
        {"title": "Travel Guide: Best European Destinations", "content": "A comprehensive guide to the top travel destinations across Europe, featuring cultural highlights and local cuisine."}
    ]

    articles = []
    for i in range(count):
        template = random.choice(article_templates)
        # Add some variation to titles/content to make them less identical
        title_suffix = f" - Update {i+1}" if random.random() < 0.3 else ""
        content_suffix = f" More details to follow. Article ID: {i+1}." if random.random() < 0.5 else ""
        articles.append({
            "id": i + 1,
            "title": template["title"] + title_suffix,
            "content": template["content"] + content_suffix
        })
    return articles

def calculate_relevance(article, negative_keywords):
    """
    Calculates a relevance score for an article based on keyword presence.
    More weight is given to specific, highly relevant terms, simulating 'AI-supported' filtering.
    """
    score = 0
    text = (article["title"] + " " + article["content"]).lower()

    # Highly relevant keywords (e.g., specific NVIDIA products/tech)
    high_value_keywords = {
        "nvidia gpu": 5, "ai chip": 5, "tensor core": 4, "cuda": 4,
        "data center": 3, "dgx": 5, "drive platform": 4, "ai computing": 4
    }
    # General relevant keywords (including "GPU" itself)
    medium_value_keywords = {
        "nvidia": 2, "gpu": 2, "artificial intelligence": 2, "machine learning": 2,
        "deep learning": 2, "semiconductor": 2, "graphics card": 2, "gaming": 1,
        "autonomous driving": 2, "metaverse": 2
    }

    # Check for high-value keywords and add their weight to the score
    for keyword, weight in high_value_keywords.items():
        if re.search(r'\b' + re.escape(keyword) + r'\b', text):
            score += weight

    # Check for medium-value keywords and add their weight
    for keyword, weight in medium_value_keywords.items():
        if re.search(r'\b' + re.escape(keyword) + r'\b', text):
            score += weight

    # Penalize for negative keywords (e.g., general finance, cooking) to reduce noise
    for keyword in negative_keywords:
        if re.search(r'\b' + re.escape(keyword) + r'\b', text):
            score -= 5 # Significant penalty

    # Ensure score doesn't go below zero
    return max(0, score)

def filter_articles(articles, negative_keywords, min_relevance_score):
    """
    Filters a list of articles based on their calculated relevance score.
    """
    filtered = []
    for article in articles:
        score = calculate_relevance(article, negative_keywords)
        if score >= min_relevance_score:
            filtered.append(article)
    return filtered

if __name__ == "__main__":
    # Define negative keywords for filtering out irrelevant content.
    # Positive keywords with weights are embedded in calculate_relevance for nuanced scoring.
    negative_keywords = [
        "stock market", "earnings report", "cooking", "travel guide",
        "software update", "processor architecture", "renewable energy",
        "smartphone sales", "economic data"
    ]

    # Generate a large number of mock articles to simulate the initial data stream.
    # The count is scaled down for demonstration purposes, similar to 5718 articles.
    total_articles_count = 50
    mock_articles = generate_mock_articles(total_articles_count)

    print(f"--- Article Filtering Demonstration ---")
    print(f"Total initial articles generated: {len(mock_articles)}")

    # Set a minimum relevance score to filter articles.
    # This threshold determines how 'strict' the filtering is, aiming to reduce
    # the volume significantly, like the article's example of 5718 to 161.
    minimum_relevance_score = 5 # Adjust this value to control filtering strictness

    # Apply the filtering process
    selected_articles = filter_articles(mock_articles, negative_keywords, minimum_relevance_score)

    print(f"\nFiltered articles (score >= {minimum_relevance_score}): {len(selected_articles)}")
    print(f"Reduction: {len(mock_articles)} -> {len(selected_articles)}")

    print("\n--- Selected Article Titles ---")
    if selected_articles:
        for i, article in enumerate(selected_articles):
            # Recalculate score for display, as it's not stored with the article
            display_score = calculate_relevance(article, negative_keywords)
            print(f"{i+1}. {article['title']} (Relevance: {display_score})")
    else:
        print("No articles met the filtering criteria. Try lowering the minimum_relevance_score.")
