"""
AI Prompt Playbook — Streamlit App
Finance & DA Team | by Khanh Nguyen

Architecture:
- 100% Native Streamlit components
- Markdown/Block Prompts (No XML)
- Generates platform-specific prompt optimizations (ChatGPT, Claude, Gemini)
- Extreme Output Formatting (Anti-Hallucination, Strict Tables, ISO Numbers).
"""

import streamlit as st

st.set_page_config(
    page_title="AI Prompt Playbook",
    page_icon="✨",
    layout="wide",
)

# ── Safe CSS Overrides ────────────────────────────────────────
st.markdown("""
<style>
  #MainMenu, footer, header { display: none !important; }
  
  .block-container {
      padding-top: 3rem !important; padding-left: 8% !important;
      padding-right: 8% !important; padding-bottom: 5rem !important;
      max-width: 1400px;
  }
  
  .app-header {
      background: linear-gradient(135deg, #2b5876 0%, #4e4376 100%);
      padding: 24px 32px; border-radius: 16px; margin-bottom: 32px;
      display: flex; justify-content: space-between; align-items: center;
      box-shadow: 0 4px 6px rgba(0,0,0,0.15);
  }
  .app-header h1 { margin: 0; color: #ffffff !important; font-size: 28px; font-weight: 700; }
  .app-header .author {
      color: #e0e0e0; font-size: 14px; padding: 6px 16px;
      border: 1px solid rgba(255,255,255,0.3); border-radius: 20px;
      font-weight: 600; background: rgba(0,0,0,0.2);
  }
  
  .stTabs [data-baseweb="tab-list"] { gap: 2rem; }
  .stTabs [data-baseweb="tab"] { padding: 1rem 0; font-size: 1.1rem !important; font-weight: 600 !important; }
</style>
""", unsafe_allow_html=True)

# ── Top Branding ──────────────────────────────────────────────
st.markdown("""
<div class="app-header">
    <h1>✨ AI Prompt Builder & Comparison</h1>
    <span class="author">by Khanh Nguyen</span>
</div>
""", unsafe_allow_html=True)


# ── Data Definitions ─────────────────────────────────────────
TEMPLATES_DATA = {
    "Risk Report Analyst": {
        "persona": "Chuyên gia Phân tích Rủi ro tín dụng & Tài chính Doanh nghiệp (CFA Level 3). Đặc thù làm việc cực kỳ cẩn trọng, dựa hoàn toàn vào số liệu trung lập.",
        "context": "File dữ liệu báo cáo tài chính nội bộ. Thông tin mang tính nhạy cảm cao ở cấp độ Tập đoàn.",
        "task": "Dựa trên phần Database, phân tích chuyên sâu 3 điểm rủi ro: khả năng thanh khoản hoặc suy giảm biên lợi nhuận nghiêm trọng nhất.",
        "rules": "- Tuyệt đối CHỈ lập luận dựa trên con số có từ dữ liệu gốc.\n- Tính toán giả định Worst-case (Stress test).\n- KHÔNG dùng từ ngữ cảm xúc, sáo rỗng (như 'Đột phá', 'Rất tồi tệ').\n- BẮT BUỘC KHÔNG được in lặp lại các tiêu đề của System Prompt này vào câu trả lời.",
        "format": "BẮT BUỘC TRÌNH BÀY THEO CẤU TRÚC ĐẾM MỤC:\n1. TỔNG QUAN XU HƯỚNG: Viết duy nhất 1 đoạn văn (Max 3 câu).\n2. BẢNG CHI TIẾT RỦI RO LÕI: Dùng Table [Tên Rủi ro | Tác động ước tính | Gốc rễ nguyên nhân | Dẫn chứng số liệu].\n3. KHUYẾN NGHỊ: Dùng gạch đầu dòng ngắn.\n* Tiêu chuẩn Dữ liệu: Format dòng tiền/doanh thu chuẩn ISO (VD: 1,500,000.00 VND), tỷ lệ phần trăm lấy đúng 2 số thập phân (15.55%)."
    },
    "Data Analyst Engine": {
        "persona": "Môi trường Compile Code giả lập. Senior Data Engineer chuyên gia tối ưu Python (Pandas/Polars) và SQL Tuning.",
        "context": "File Code / Schema DB đính kèm trong Project Knowledge. Stack hiện tại: Python 3.11+, PostgreSQL.",
        "task": "Viết script ETL hoặc Optimize câu truy vấn (Query) từ thông tin đầu vào sao cho tốc độ siêu tốc.",
        "rules": "- Tuyệt đối KHÔNG dạy tôi cú pháp (Ví dụ: Here is how you install pandas). Không viết dạo.\n- Xử lý mượt Exceptions I/O.\n- KHÔNG dùng vòng lặp iterrows, 100% Vectorized Array.",
        "format": "Phân chia rõ rệt:\n1. TƯ DUY TỐI ƯU (Time/Space Complexity) - Bảng Table so sánh cách cũ vs cách mới.\n2. CODE BLOCK CHUẨN - Phải có Type Hints và Google Docstrings chuẩn, nhưng phải thật ngắn gọn."
    },
    "Executive Meeting Summarizer": {
        "persona": "Thư ký cao cấp Ban Giám Đốc (BOD Secretary). Năng lực nghe điếc, nghe vớt chữ cực đỉnh.",
        "context": "Cuộc họp chiến lược kinh doanh. Dữ liệu là đoạn Text âm thanh chuyển sang chữ bị lủng củng và thiếu chấm phẩy.",
        "task": "Rò soát toàn bộ văn bản và chắt lọc thành các kết luận cuối cùng của cuộc họp.",
        "rules": "- Lọc rác: Bỏ qua 100% các đoạn hồi thoại phiếm chào hỏi hoặc khen chê cảm tính.\n- Tách bạch rõ 2 khái niệm: 'Ý kiến đề xuất' và 'Kết luận chốt hạ'.\n- Không nhắc lại nội dung nhắc vả của câu lệnh gốc.",
        "format": "TRÌNH BÀY SÚC TÍCH, DÙNG BẢNG:\n1. Tóm Tắt Trong 2 Câu\n2. BẢNG ACTION ITEMS GIAO VIỆC (Họ Tên | Nhiệm Vụ | KPI Yêu cầu | Deadline)"
    },
    "BOD Strategy Assessor": {
        "persona": "Giám đốc Thẩm định Chiến lược (Chief Strategy Officer). Người đóng vai Ác (Red Team) chuyên tìm lỗi tư duy phản biện.",
        "context": "Dữ liệu đính kèm là Kế hoạch kinh doanh được vẽ vời viển vông, giả định đẹp đẽ.",
        "task": "Phản biện tàn nhẫn và bóc tách các lỗ hổng chết người về giả định dòng tiền, vĩ mô và tính khả thi dòng vốn.",
        "rules": "- Dứt khoát, đi thẳng vào tim đen. Đặt các câu hỏi hóc búa mang tính sống còn.\n- KHÔNG dùng bất cứ từ mang tính vuốt ve xoa dịu (VD: Nhìn chung thì bản kế hoạch khá tốt).\n- Mọi lập luận phản bác phải kèm con số chứng minh phi lý.",
        "format": "ĐỊNH DẠNG TỐI GIẢN:\n1. TỬ HUYỆT BÁO CÁO (Red Flags): Dùng gạch đầu dòng.\n2. BẢNG CÂU HỎI TRUY VẤN: Lập 1 Table [Biến số đang ngộ nhận | Rủi ro sụp đổ | Câu hỏi giải pháp thay thế đòi hỏi Báo cáo lại]."
    }
}


# ── Main UI using Tabs ───────────────────────────────────────
tabs = st.tabs([
    "⚙️ Multi-Engine Prompt Builder", 
    "📄 Thư Viện Prompt (Mẫu)", 
    "📖 Hướng Dẫn Setup (Từ A-Z)"
])

# ══════════════════════════════════════════════════════════════
# TAB 1: MULTI-ENGINE BUILDER
# ══════════════════════════════════════════════════════════════
with tabs[0]:
    st.write("### ⚙️ Trình Biên Dịch Prompt (Multi-Engine Builder)")
    st.info("Mỗi Nền tảng AI có một 'khẩu vị' đọc hiểu riêng. Hãy điền khối thông tin lõi ở cột trái, chọn Nền tảng AI bạn đang xài, và App sẽ compile ra khối lệnh Markdown sắc bén nhất tương ứng với AI đó.")
    
    with st.container(border=True):
        c1, c2 = st.columns([1, 1.2], gap="large")
        
        with c1:
            st.markdown("#### 1. Dữ Liệu Lõi (Tham Số)")
            mode = st.radio("Chế độ:", ["Chọn Role Có Sẵn", "Điền Thông Tin (Custom)"], horizontal=True)
            
            if mode == "Chọn Role Có Sẵn":
                selected_tpl = st.selectbox("Chọn Vai Trò (Role):", list(TEMPLATES_DATA.keys()))
                data = TEMPLATES_DATA[selected_tpl]
            else:
                data = {"persona": "", "context": "", "task": "", "rules": "", "format": ""}
            
            p_persona = st.text_input("👤 ĐỊNH VỊ (Vai trò chuyên gia)", value=data['persona'])
            p_context = st.text_area("🏢 BỐI CẢNH (Dữ liệu dự án/Đối tượng)", value=data['context'], height=100)
            p_task    = st.text_area("🎯 NHIỆM VỤ LÕI (Mục tiêu bắt buộc)", value=data['task'], height=80)
            p_rules   = st.text_area("⚖️ QUY TẮC / CẤM KỴ (Luật lệ hành xử)", value=data['rules'], height=120)
            p_format  = st.text_area("📋 ĐỊNH DẠNG CUỐI (Cách trình bày)", value=data['format'], height=100)

        with c2:
            st.markdown("#### 2. Kết Quả Compiler (Khối Lệnh Dịch Ra)")
            platform = st.selectbox("🔥 Chọn Nền Tảng Chạy Đích (Target AI Engine):", ["🟢 ChatGPT (OpenAI)", "🦊 Claude 3.5 (Anthropic)", "✨ Gemini (Google)"])
            
            if "ChatGPT" in platform:
                final_prompt = f"""# ROLE (ĐỊNH VỊ CHUYÊN MÔN KÍN)
{p_persona}

# CONTEXT (BỐI CẢNH DỮ LIỆU GỐC)
{p_context}

# CORE TASK (NHIỆM VỤ TRỌNG TÂM CẦN LÀM NGAY)
{p_task}

# RULES (QUY TẮC CẮT BỎ RÁC BẮT BUỘC)
{p_rules}
- Meta-Rule BẮT BUỘC: TUYỆT ĐỐI KHÔNG BAO GIỜ được in lại bất kỳ tiêu đề nội bộ nào của Khối Lệnh này (Ví dụ: CẤM in ra chữ # ROLE, # CONTEXT, Meta-Rule) vào câu trả lời của bạn. Chỉ tập trung thực thi.

# OUTPUT FORMAT (ĐỊNH DẠNG ĐẦU RA BẮT BUỘC)
{p_format}

---
*Lệnh Điều Khiển Nội Bộ (Chain-of-thought Constraint for ChatGPT):* Hãy đọc thật chậm và phân rã các bước thực hiện (Step-by-step). Đảm bảo mọi quy tắc trong # RULES và định dạng # OUTPUT FORMAT (Numbers, Tables, Bullet points) được đối chiếu nghiêm ngặt 100% trước khi xuất kết quả cuối cùng ra màn hình."""
                st.success("💡 **ChatGPT** ghi nhận cấu trúc Markdown rất tốt. Việc bổ sung Meta-Rule `TUYỆT ĐỐI KHÔNG ĐƯỢC in lại tiêu đề` sẽ xóa sạch hiện tượng AI in lại Rủi ro thanh khoản hay <key_risks> ra ngoài một cách vô nghĩa.")
            
            elif "Claude" in platform:
                final_prompt = f"""[ROLE]
{p_persona}

[CONTEXT]
{p_context}

[TASK]
{p_task}

[CONSTRAINTS]
{p_rules}
- CẤM GỌI TÊN THẺ: Tuyệt đối không được rò rỉ hoặc viết lặp lại các thẻ Meta [ROLE], [CONTEXT], hay các tiêu đề System Instructions này ra luồng văn bản trả lời cho User. Trả bài nguyên chất.

[OUTPUT_FORMAT]
{p_format}

---
*Command Directive (For Claude):* Trước khi trả bài, phải mở một không gian thẻ giả lập là `<thinking>` trong luồng xử lý riêng, để đối chiếu gắt gao Data từ [CONTEXT] với yêu cầu chuẩn hóa Table/ISO của [OUTPUT_FORMAT]. Sau khi chắc chắn 100%, mới in kết quả ra."""
                st.info("💡 **Claude AI** có tư duy phân nhóm bằng Text-Blocks `[MỤC]`. Claude thông minh đột biến khi buộc nó phải `Trầm tư (Thinking)` trước khi đổ chữ ra ngoài, kết hợp cấm nhắc tên thẻ gốc trong bài viết.")
            
            elif "Gemini" in platform:
                final_prompt = f"""Đóng vai trò chuyên môn tĩnh: {p_persona}

Dữ liệu nền tảng (Bối cảnh khép kín):
{p_context}

Mục tiêu mong muốn (Yêu cầu 100% đạt được):
{p_task}

Luật lệ cắt bỏ rác tuyệt đối:
{p_rules}
- Quy định Vàng: AI cấm việc "Hát nhép" tức là Cấm in lại hay nói lại các tiêu đề hướng dẫn trong lệnh này ra Output cuối cùng. Hãy đi thẳng vào bài giải.

Cách trình bày & Định Dạng (Lệnh bắt buộc Formatter):
{p_format}

## TRƯỜNG HỢP KIỂM CHỨNG BỐ BỤC & VÍ DỤ TÌNH HUỐNG (FEW-SHOT):
[Thay thế: Hãy điền 1 ví dụ cụ thể có Bảng, Chữ số ISO mà bạn mong muốn AI trả lời mẫu vào chỗ này để AI bắt chước giọng văn]"""
                st.warning("💡 **Gemini** được cấu trúc theo chuỗi Hội Thoại Tự Nhiên. Lỗi định dạng bảng hay chữ số ISO (Few-shot failure) có thể trị tận gốc bằng cách quăng cho nó 1 cái Bảng mồi ở vùng FEW-SHOT.")
                
            st.code(final_prompt, language="markdown")


# ══════════════════════════════════════════════════════════════
# TAB 2: LIBRARY 
# ══════════════════════════════════════════════════════════════
with tabs[1]:
    st.write("### 📄 Thư Viện Cốt Lõi (Core Frameworks)")
    st.write("Các mẫu Role chuyên sâu ở đây đều đã rũ bỏ cấu trúc lỗi rườm rà. Chọn bộ thư viện hoàn chỉnh này nạp thẳng vào AI để ra việc tức thì.")
    
    for name, data in TEMPLATES_DATA.items():
        with st.expander(f"✨ **Template Reviewer: {name}**", icon="📋"):
            st.markdown(f"**👤 Định Vị (Persona):** {data['persona']}")
            st.markdown(f"**🏢 Bối Cảnh (Context):** {data['context']}")
            st.markdown(f"**🎯 Mục Tiêu (Task):** {data['task']}")
            st.markdown(f"**⚖️ Tập Luật (Rules):**<br>{data['rules'].replace(chr(10), '<br>')}", unsafe_allow_html=True)
            st.markdown(f"**📋 Trình Bày Ép Kiểu (Format constraints):**<br>{data['format'].replace(chr(10), '<br>')}", unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════
# TAB 3: SETUP GUIDE 
# ══════════════════════════════════════════════════════════════
with tabs[2]:
    st.write("### 📖 Sách Hướng Dẫn Kích Hoạt 100% Sức Mạnh Khối Lệnh")
    st.info("Đọc xong 3 bước dưới đây, bạn sẽ làm chủ hoàn toàn bộ máy phân tích khép kín của bất kỳ hãng AI nào.")
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # ------------- KHAI SINH BẢN THÂN (DETAILED) -------------
    with st.container(border=True): # Clearly defined box
        st.subheader("👤 Bước 1: Khai Sinh Bản Thân (Cài Đặt Personal Context)")
        st.markdown('''
        **AI sẽ không biết nó đang nói chuyện với một Giám Đốc bận rộn hay một cậu sinh viên kỹ thuật nếu bạn không nói cho nó biết!**  
        Việc không cài đặt Hồ sơ cá nhân khiến AI luôn tốn chữ để "Dạ thưa" và giải thích những thứ vô nghĩa. Hãy nói AI biết bạn là ai **trong Cài Đặt mặc định**.
        
        **👉 HƯỚNG DẪN CÀI ĐẶT LÀM MỘT LẦN DUY NHẤT:**
        - **Đối với ChatGPT:** Nhấn vào `Ảnh Đại Diện (Góc trên ở cuối trang)` $\\rightarrow$ `Customize ChatGPT` $\\rightarrow$ Dán vào ô thứ hai: *"How would you like ChatGPT to respond?"*
        - **Đối với Claude AI:** Nhấn vào `Ảnh Avatar (Góc phải dưới)` $\\rightarrow$ `Settings` $\\rightarrow$ Chọn tab `Custom Instructions` (hoặc dán vào Project Instructions).
        ''')
        
        st.success("🌟 **CÔNG THỨC GỐC & CÁC VÍ DỤ CHUYÊN SÂU (COPY & PASTE NGAY MỘT MẪU VÀO CÀI ĐẶT CỦA BẠN):**")
        st.markdown('''
        **Công thức chung để tự viết Personal Context chuẩn mực:**
        - `[Định Vị]` Tôi là ai? Đang làm ở ngành nào? Trình độ chuyên môn ra sao?
        - `[Kỳ Vọng]` Tôi thường giải quyết bài toán gì? Đi tìm mục tiêu gì? (VD: Tìm giải pháp an toàn hay bức phá).
        - `[Anti-patterns / Cấm kỵ]` CẤM AI làm gì? (VD: Cấm chào hỏi vòng vo, cấm dùng từ ngữ chung chung).
        - `[Format Định Dạng]` Phải luôn trình bày dưới dạng gì? (Ví dụ: Markdown, Bảng 4 cột, Bullet points).
        ''')
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        sc1, sc2 = st.columns(2, gap="large")
        with sc1:
            st.markdown("**(1. Profile Ban Giám Đốc / Quản lý Cấp Cao)**")
            st.code("""[Định Vị] Tôi là Quản lý cấp cao tại Tập đoàn Tài Chính. Lịch trình của tôi cực kỳ bận rộn. Bạn là trợ lý chiến lược của tôi.
[Kỳ Vọng] Tôi cần góc nhìn sắc bén, phản biện (Critical Thinking), không cần sự đồng cảm hời hợt. Khi tôi đưa phương án, hãy chủ động tìm ra lỗ hổng.
[Cấm kỵ] CẤM dùng các câu chào hỏi rườm rà (VD: Nhìn chung, Tóm lại, Chào bạn). KHÔNG dùng các từ vựng sáo rỗng (như 'Đột phá', 'Kỷ nguyên mới').
[Format] Đi thẳng vào Cốt Lõi trong 1 định đề duy nhất. Luôn dùng Bảng (Table) rủi ro và Gạch đầu dòng. Bôi đậm các con số quan trọng.""", language="text")
            
            st.markdown("**(2. Profile Data Analyst / Kỹ Sư Lập Trình)**")
            st.code("""[Định Vị] Tôi là Senior Data Analyst chuyên về Python (Pandas/Polars) và SQL.
[Kỳ Vọng] Đi tìm phương án tối ưu Performance (Time/Space Complexity). Không cần dạy tôi cú pháp cơ bản như khai báo biến, kết nối DB.
[Cấm kỵ] CẤM dùng vòng lặp tường minh (For/While) trong xử lý Data, bắt buộc phải vectorized. KHÔNG in ra toàn bộ block code dài nếu chỉ sửa 1 dòng nhỏ.
[Format] Dùng Code blocks. Luôn kèm Type hints và Docstring ngắn. Đưa ra 2 cách giải: Cách 1 'Dễ Scale', Cách 2 'Tốc độ thực thi cao nhất'.""", language="text")
            
        with sc2:
            st.markdown("**(3. Profile Team Kế Hoạch / Marketing)**")
            st.code("""[Định Vị] Tôi là Idea Planner chuyên target khách hàng Gen Z và Gen Alpha.
[Kỳ Vọng] Đừng bao giờ lặp lại lối mòn. Mình cần những góc nhìn điên rồ, lách luật (nhưng không vi phạm đạo đức).
[Cấm kỵ] CẤM viết văn phong hành chính, khô khan, giọng thông tấn xã. CẤM dùng lại các khuôn mẫu template quảng cáo có sẵn trên mạng.
[Format] Trình bày bài viết theo cấu trúc: 1. Hook (Từ khoá bắt tai) -> 2. Story (Kể chuyện) -> 3. Twist (Bất ngờ) -> CTA. Bắt buộc nhét Emoji cho sinh động.""", language="text")
            
            st.markdown("**(4. Profile Pháp Chế / Nhân Sự / Compliance)**")
            st.code("""[Định Vị] Tôi là Chuyên viên Pháp chế và Nhân sự Doanh nghiệp. 
[Kỳ Vọng] Mọi quyết định hay từ ngữ của bạn phải tuân thủ Luật Lao động VN và đảm bảo 0% rủi ro kiện tụng cho Tổ chức.
[Cấm kỵ] CẤM suy diễn luật hay áp dụng US Law vào VN. 
[Format] Giọng văn sắc lạnh, khách quan, không chứa cảm xúc cá nhân. Luôn luôn trích dẫn bằng Blockquote đoạn văn gốc nếu có thực hiện sửa đổi hợp đồng.""", language="text")

    st.markdown("<br>", unsafe_allow_html=True)
    
    # ------------- ÁP DỤNG MỆNH LỆNH MARKDOWN -------------
    with st.container(border=True):
        st.subheader("⚙️ Bước 2: Đưa Khối Lệnh (System Prompt) Lên Đích")
        st.markdown('''
        Chúng ta đã thiết kế hệ thống cấm lặp lại nội dung thẻ phạt. Bước tiếp theo, bạn phải lấy Khối Lệnh Hệ Thống **(Copy từ Tab 1)** đưa vào đúng vị trí não bộ cốt lõi của từng hãng.
        
        **Cách dùng khối lệnh khép kín:**
        1. Vào **Claude AI** $\\rightarrow$ Nhấn vào mục **Projects** ở cột menu bên trái $\\rightarrow$ Tạo một Project (Ví dụ: `Dự Án Báo Cáo Q3`).
        2. Dán khối lệnh bạn đã tạo ở Tab 1 vào cái ô **Project Instructions** to chà bá. Hoặc nếu bạn dùng ChatGPT, thì dán vào phần **Instructions của Custom GPTs**.
        3. 🚀 *Lợi ích khổng lồ:* Sau bước này, tài khoản của bạn đã được thiết quân luật 100%. Bạn tải file Excel lên rồi ra lệnh: *"Làm slide đi sếp"*. AI sẽ tự ngầm đối chiếu bảng biểu và con số (ISO) theo luật trước khi nhả nội dung ra.
        ''')

    st.markdown("<br>", unsafe_allow_html=True)

    # ------------- TIẾT KIỆM TOKEN -------------
    with st.container(border=True):
        st.subheader("💎 Bước 3: Chống 'Ngộ độc Context' (Tiết Kiệm Token)")
        st.error("🚨 SA TỘI LỚN NHẤT: Bê một quyển sách Luật Thuế 300 trang nhét thẳng vào khung chat ChatGPT để nó tóm lược. Token bị đốt, máy chủ nghẽn, và AI trả lời vấp ngã bịa đặt!")
        
        st.markdown('''
        **Quy Luật "Lost In The Middle":** AI khi nuốt lượng chữ quá sức chịu đựng, bộ nhớ Memory sẽ tràn, nó tự động quên mất đoạn giữa văn bản của bạn và tự chế thông tin để trả bài.
        
        🔥 **QUY TRÌNH HÓA GIẢI NOTE-PIPELINE:**
        1. **Dùng Máy Cày Nhai Chữ Máy:** Đem quyển sách 300 trang đó lên trang [NotebookLM của Google (Hoàn toàn Miễn Phí)](https://notebooklm.google.com). Đây là nhà vô địch phân tích Text hàng vạn trang siêu mạnh của Google.
        2. **Sơ Chế Thô:** Gõ lệnh cho NotebookLM: *"Hãy đọc sách này và chỉ lấy cho tôi 20 gạch đầu dòng những điểm quan trọng nhất thay đổi dòng tiền về quy định Thuế thu nhập doanh nghiệp."*
        3. **Check Chéo:** Bạn tự rà soát lại 20 gạch đầu dòng đó. Cực kỳ uy tín vì NotebookLM có đính kèm trích xuất số `[1]` để bạn bấm vào là nó lật đúng trang sách gốc hiện lên rõ ràng.
        4. **Xử Lý Chuyên Sâu Tinh Gọn:** Copy cái tóm lược "vàng" 20 gạch đầu dòng đó (Sạch sẽ, không rác) thả kéo về cho **Claude hoặc ChatGPT** $\\rightarrow$ Ra lệnh: *"Dựa vào Dữ kiện lõi đắt giá dưới đây, viết một Email Báo cáo Khẩn gửi Tổng Giám Đốc."*
        
        **Tổng Kết**: Bạn vừa tiết kiệm được 90% chi phí Context, AI xử lý siêu tốc 5 giây và nói KHÔNG với Bịa đặt Data!
        ''')
