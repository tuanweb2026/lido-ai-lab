import re
import urllib.parse

class GlobalEnglishScriptWriterAgent:
    """
    AGENT BIÊN KỊCH CHUYÊN BIỆT CHO SQUAD GLOBAL (100% ENGLISH):
    - Soạn thảo toàn bộ kịch bản, phụ đề, lệnh Terminal và headline 100% bằng tiếng Anh chuẩn.
    - Đa dạng hóa cấu trúc narrative, bám sát các thực thể công nghệ AI (OpenAI, Anthropic, Nvidia, Google, DeepSeek...).
    """
    def __init__(self, channel_name="@LidoAILab"):
        self.channel_name = channel_name

    def clean_title(self, raw_title):
        return re.sub(r'\s*-\s*[A-Za-z0-9. -]+$', '', raw_title).strip()

    def identify_entity(self, text):
        t_low = text.lower()
        known = [
            "OpenAI", "ChatGPT", "Claude", "Anthropic", "Tesla", "Optimus",
            "Google", "Gemini", "Cursor", "DeepSeek", "Sora", "Nvidia",
            "Meta", "YouTube", "Palo Alto Networks", "GitHub Copilot", "Devin", "Grok"
        ]
        found = [b for b in known if b.lower() in t_low]
        return found[0] if found else "AI Technology"

    def generate_script_from_topic(self, topic):
        raw_title = topic.get("title", "")
        clean_t = self.clean_title(raw_title)
        t_low = clean_t.lower()
        entity = self.identify_entity(clean_t)

        # 1. MCP / Protocol / Agentic workflow
        if any(k in t_low for k in ["mcp", "protocol", "agentic", "workflow"]):
            badge = "AGENTIC ECOSYSTEM"
            h1 = f"{entity.upper()} EXPANDS MCP ARCHITECTURE"
            t1 = f"Major architectural milestone in enterprise AI: {clean_t}!"
            h2 = "SECURE PROTOCOL INTEGRATION"
            t2 = "Instead of isolated chat prompts, agents now interface directly with operational databases, real-time dispatch systems, and external APIs."
            h3 = "TRANSITION TO AUTONOMOUS COMMERCE"
            t3 = "Standardizing execution protocols unlocks autonomous operations across cloud and on-premise infrastructure without human middleware."
            h4 = "THE ROADMAP AHEAD"
            t4 = "Engineering teams adopting open agent protocols will outpace rigid legacy workflows with orders of magnitude higher speed!"
            cmd = f"mcp-gateway --connect-runtime --client {entity.lower()}"
            status = "[MCP GATEWAY] Initializing verified secure handshake..."
            res = "✓ Connected to distributed agent network protocol"
            stamp = "🌐 MCP PROTOCOL"
            kws = [f"{entity} agent protocol software", "Cloud enterprise architecture data flow"]

        # 2. Nvidia / Hardware / Silicon safety
        elif "nvidia" in t_low or "silicon" in t_low or "gpu" in t_low:
            badge = "HARDWARE & SILICON"
            h1 = f"NVIDIA ENFORCES HARDWARE SAFETY"
            t1 = f"Critical hardware news coming directly from Silicon Valley: {clean_t}!"
            h2 = "GUARDRAILS AT THE SILICON LEVEL"
            t2 = "Nvidia is embedding safety verification logic directly into enterprise accelerators, preventing unauthorized agent drift at physical hardware speeds."
            h3 = "ELIMINATING SOFTWARE OVERHEAD"
            t3 = "By handling policy evaluation on the silicon layer, enterprise workloads remain mathematically secure without sacrificing compute throughput."
            h4 = "NEXT-GEN ENTERPRISE STANDARDS"
            t4 = "Hardware-enforced safety marks a decisive transition from experimental sandbox models to mission-critical industrial deployments!"
            cmd = "nvidia-smi --enforce-agent-safety --audit-level strict"
            status = "[GPU AUDIT] Scanning active compute kernels for compliance..."
            res = "✓ 100% hardware-isolated memory channels validated"
            stamp = "⚡ SILICON GUARD"
            kws = ["Nvidia Blackwell GPU server rack glowing", "Enterprise datacenter supercomputer hardware"]

        # 3. Security Breach / Exploit / Brute-force
        elif any(k in t_low for k in ["breach", "bruteforce", "leak", "security", "hack"]):
            badge = "CYBERSECURITY ALERT"
            h1 = f"AI AGENT EXPLOIT DETECTED"
            t1 = f"Urgent cybersecurity disclosure rocking the tech community: {clean_t}!"
            h2 = "UNMONITORED AGENT RECURSION"
            t2 = "Security analysts discovered autonomous agents repeatedly executing unauthorized traversal scripts without human intervention."
            h3 = "THE PERILS OF PERMISSIVE SCOPES"
            t3 = "Granting autonomous computer-use privileges without bounded network policies creates unpredictable lateral attack vectors."
            h4 = "IMMEDIATE MITIGATION REQUIRED"
            t4 = "DevOps teams must immediately enforce strict rate limits, verify API scopes, and require cryptographic authorization tokens!"
            cmd = "agent-firewall --quarantine-rogue-nodes --revoke-tokens"
            status = "[FIREWALL] Intercepting suspicious outbound agent requests..."
            res = "🔒 Threat contained: 42 rogue endpoints isolated"
            stamp = "🚨 SECURITY BREACH"
            kws = ["Cybersecurity terminal lock screen red alert", "Hacker network security encrypted server"]

        # 4. Model Benchmarks / Release / Claude vs GPT
        elif any(k in t_low for k in ["beats", "benchmarks", "claude", "gpt-", "opus", "sonnet"]):
            badge = "BENCHMARK WAR 2026"
            h1 = f"FRONTIER MODEL SHOWDOWN"
            t1 = f"The battle for generative intelligence reaches unprecedented heights: {clean_t}!"
            h2 = "COST-TO-PERFORMANCE REVOLUTION"
            t2 = "Benchmark audits verify breakthrough reasoning capabilities delivered at a tiny fraction of previous generation API inference costs."
            h3 = "AGENTIC CODE EXECUTION"
            t3 = "Enhanced multi-turn reasoning and tool orchestration make these updated weights significantly more reliable for production environments."
            h4 = "ADOPTING THE LEADING MODEL"
            t4 = "Benchmark your internal evaluation suites today to capitalize on immense cost reductions and accelerated inference velocities!"
            cmd = "eval-harness --run-benchmark-suite --compare-frontier"
            status = "[EVAL] Executing 10,000 multi-turn coding benchmarks..."
            res = "✓ Accuracy: 94.8% at 65% reduced token latency"
            stamp = "🏆 BENCHMARK LEADER"
            kws = [f"{entity} benchmark evaluation chart", "Artificial intelligence neural network graph"]

        # 5. Default General Tech
        else:
            badge = f"{entity.upper()} SPOTLIGHT"
            h1 = f"NEW BREAKTHROUGH: {entity.upper()}"
            t1 = f"Significant technological update officially unveiled: {clean_t}!"
            h2 = "SOLVING REAL INDUSTRY BOTTLENECKS"
            t2 = f"This strategic initiative by {entity} targets foundational workflow frictions, delivering substantially enhanced stability and execution velocity."
            h3 = "SEAMLESS ECOSYSTEM DEPLOYMENT"
            t3 = "Engineers can rapidly deploy this capability across active stacks without rewriting existing infrastructure pipelines."
            h4 = "STAYING AHEAD IN 2026"
            t4 = f"Follow the rapid evolution of {entity} closely to maintain strategic advantages in this fast-moving landscape!"
            cmd = f"deploy-module --target {entity.lower()} --status-check"
            status = "[RUNTIME] Verifying production deployment status..."
            res = "✓ Successfully deployed across multi-region clusters"
            stamp = "🚀 TECH BREAKTHROUGH"
            kws = [f"{entity} technology presentation stage", "Futuristic technology user interface digital"]

        scenes = [
            {"scene_id": 1, "headline": h1, "metric_badge": badge, "text": t1, "overlay_data": h1, "search_keywords": kws},
            {"scene_id": 2, "headline": h2, "metric_badge": badge, "text": t2, "overlay_data": h2, "search_keywords": kws},
            {"scene_id": 3, "headline": h3, "metric_badge": badge, "text": t3, "overlay_data": h3, "search_keywords": kws},
            {"scene_id": 4, "headline": h4, "metric_badge": badge, "text": t4, "overlay_data": h4, "search_keywords": kws},
            {
                "scene_id": 5,
                "headline": "EXCLUSIVE TECH INTELLIGENCE",
                "metric_badge": "LIDO AI LAB",
                "text": "Subscribe to Lido AI Lab today to stay ahead of the most powerful AI breakthroughs!",
                "overlay_data": "SUBSCRIBE @LidoAILab",
                "search_keywords": ["YouTube subscribe button glowing neon red", "Modern tech creator studio setup"]
            }
        ]

        video_title = f"{badge}: {clean_t[:65]}! 🚀⚡ #Shorts #LidoAILab #AI"
        workflow_metadata = {
            "badge_title": badge,
            "step1": h1,
            "step2": h2,
            "term_title": f"terminal · {entity.lower()} runtime",
            "code_cmd": cmd,
            "code_status": status,
            "code_result": res,
            "step4": h4,
            "stamp_text": stamp
        }

        return {
            "title": video_title,
            "scenes": scenes,
            "workflow_metadata": workflow_metadata,
            "full_voice_text": " ".join([s["text"] for s in scenes])
        }
