"""
AI Prompt Playbook — Streamlit App
Finance & DA Team | by Khanh Nguyen

Architecture:
- 100% Native Streamlit components for perfect Light/Dark mode contrast
- Heavy use of st.container(border=True) to fix the "no clear boxes" issue
- Generous padding to fix the "too close to edge" issue
- Extremely detailed guide on setting up Personal Context.
"""

import streamlit as st

st.set_page_config(
    page_title="AI Prompt Playbook",
    page_icon="✨",
    layout="wide",
)

# ── Safe CSS Overrides (Preserving Streamlit's Perfect Contrast) ──
st.markdown("""
<style>
  #MainMenu, footer, header { display: none !important; }
  
  /* Fix content being too close to the edges */
  .block-container {
      padding-top: 3rem !important;
      padding-left: 8% !important;
      padding-right: 8% !important;
      padding-bottom: 5rem !important;
      max-width: 1400px;
  }
  
  /* Clean App Header */
  .app-header {
      background: linear-gradient(135deg, #2b5876 0%, #4e4376 100%);
      padding: 24px 32px;
      border-radius: 16px;
      margin-bottom: 32px;
      display: flex;
      justify-content: space-between;
      align-items: center;
      box-shadow: 0 4px 6px rgba(0,0,0,0.15);
  }
  .app-header h1 {
      margin: 0;
      color: #ffffff !important;
      font-size: 28px;
      font-weight: 700;
  }
  .app-header .author {
      color: #e0e0e0;
      font-size: 14px;
      padding: 6px 16px;
      border: 1px solid rgba(255,255,255,0.3);
      border-radius: 20px;
      font-weight: 600;
      background: rgba(0,0,0,0.2);
  }
  
  /* Adjust Tabs styling to match native feel but larger */
  .stTabs [data-baseweb="tab-list"] {
      gap: 2rem;
  }
  .stTabs [data-baseweb="tab"] {
      padding: 1rem 0;
      font-size: 1.1rem !important;
      font-weight: 600 !important;
  }
</style>
""", unsafe_allow_html=True)

# ── Top Branding ─────────────────────────────────────────────
st.markdown("""
<div class="app-header">
    <h1>✨ AI Prompt Playbook</h1>
    <span class="author">by Khanh Nguyen</span>
</div>
""", unsafe_allow_html=True)


# ── Data Definitions ─────────────────────────────────────────
TEMPLATES_DATA = {
    "Risk Report Analyst": {
        "persona": "Chuyên gia Phân tích Rủi ro Tín dụng cấp cao, CFA-level.",
        "context": "Tập đoàn đa ngành, dữ liệu tài chính lấy từ SQL Server.",
        "task": "Trên cơ sở dữ liệu cung cấp, phân tích 3 rủi ro tín dụng hoặc thanh khoản lớn nhất.",
        "rules": "1. Chỉ lập luận dựa trên số liệu thực tế trong bảng.\n2. Phân tích cả trường hợp xấu nhất (stress-test).\n3. Rõ ràng, minh bạch, có cảnh báo cụ thể.",
        "format": "Markdown.\n<summary>\n<key_risks>\n<action_recommendations>"
    },
    "Data Analyst Engine": {
        "persona": "Senior Data Analyst thông thạo Python & Pandas 2.0.",
        "context": "Schema DB đính kèm trong Project Knowledge. Stack: Python 3.11+.",
        "task": "Viết script ETL xử lý data, tối ưu hóa code theo yêu cầu của User.",
        "rules": "1. Luôn đính kèm type hints.\n2. Bắt buộc xử lý exceptions khi đọc/ghi file.\n3. Dùng vectorized operations, KHÔNG dùng vòng lặp iterrows.",
        "format": "Hướng giải quyết -> Python Script Block -> Complexity Analysis."
    },
    "Executive Meeting Summarizer": {
        "persona": "Thư ký cao cấp Ban Giám Đốc (BOD Secretary).",
        "context": "Cuộc họp chiến lược kinh doanh quý 3. File Transcript (âm thanh chuyển chữ) dán kèm.",
        "task": "Trích xuất quyết định đã chốt, và gán tên người chịu trách nhiệm (PIC).",
        "rules": "1. Bỏ qua hội thoại phiếm.\n2. Phân biệt rõ 'Ý kiến đề xuất' và 'Quyết định đã duyệt'.\n3. Trình bày cực kỳ súc tích.",
        "format": "Markdown. \n## Tóm Tắt Cuộc Họp\n## Quyết Định Đi Đến\n## Action Items (Bảng)"
    },
    "BOD Strategy Assessor": {
        "persona": "BOD Strategy Advisor. Cố vấn chiến lược cấp C-level từ McKinsey.",
        "context": "Sếp trình bản Kế hoạch kinh doanh 5 năm.",
        "task": "Critical Review (Đóng vai Ác). Tìm ra các lỗ hổng về dòng tiền và giả định thị trường.",
        "rules": "1. Đặt câu hỏi hóc búa mang tính sống còn.\n2. Không dùng mỹ từ mượt mà, phải thật trực diện.\n3. Dùng Bullet list để đọc nhanh.",
        "format": "Markdown: 1. Đánh Giá Chung -> 2. The Red Flags -> 3. Câu Hỏi Buộc Phải Trả Lời."
    }
}


# ── Main UI using Tabs ───────────────────────────────────────
tabs = st.tabs([
    "⚙️ Khởi Tạo Prompt (Builder)", 
    "📄 Thư Viện Prompt (Mẫu)", 
    "📖 Hướng Dẫn Setup (Từ A-Z)"
])

# ══════════════════════════════════════════════════════════════
# TAB 1: BUILDER
# ══════════════════════════════════════════════════════════════
with tabs[0]:
    st.write("### ⚙️ Tạo System Prompt Chuẩn (Google Framework)")
    st.info("Sử dụng thẻ XML (`<persona>`, `<task>`) là cách duy nhất để khóa tư duy AI 100% không đi trật đường ray.")
    
    with st.container(border=True): # Clear box
        c1, c2 = st.columns([1, 1.2], gap="large")
        
        with c1:
            st.markdown("#### Tính Năng Điều Điển")
            mode = st.radio("Chế độ:", ["Chọn Role Có Sẵn", "Điền Thông Tin (Custom)"], horizontal=True)
            
            if mode == "Chọn Role Có Sẵn":
                # Clear UI distinction
                selected_tpl = st.selectbox("Chọn Vai Trò (Role):", list(TEMPLATES_DATA.keys()))
                data = TEMPLATES_DATA[selected_tpl]
            else:
                data = {"persona": "", "context": "", "task": "", "rules": "", "format": ""}
            
            p_persona = st.text_input("👤 <persona> (Định vị chuyên gia)", value=data['persona'])
            p_context = st.text_area("🏢 <context> (Bối cảnh dữ liệu dự án)", value=data['context'], height=100)
            p_task    = st.text_area("🎯 <task> (Nhiệm vụ lõi)", value=data['task'], height=80)
            p_rules   = st.text_area("⚖️ <rules> (Quy định bắt buộc)", value=data['rules'], height=120)
            p_format  = st.text_area("📋 <format_and_examples>", value=data['format'], height=80)

        with c2:
            st.markdown("#### Kết Quả Đầu Ra (XML)")
            st.success("💡 **Copy nguyên khối XML này**, dán vào `Project Instructions` của Claude hoặc `Custom Instructions` của ChatGPT.")
            
            final_prompt = f"""<persona>
{p_persona}
</persona>

<context>
{p_context}
</context>

<task>
{p_task}
</task>

<rules>
{p_rules}
</rules>

<format_and_examples>
{p_format}
</format_and_examples>"""
            st.code(final_prompt, language="xml")


# ══════════════════════════════════════════════════════════════
# TAB 2: LIBRARY 
# ══════════════════════════════════════════════════════════════
with tabs[1]:
    st.write("### 📄 Thư Viện Design Pattern")
    st.write("Thư viện các Role thiết kế sẵn, phân mảnh chi tiết bằng thẻ XML. Chọn thư viện này nạp thẳng vào AI để ra việc tức thì.")
    
    st.markdown("<br>", unsafe_allow_html=True)
    # Use native expanders instead of confusing custom CSS cards which might be low contrast
    for name, data in TEMPLATES_DATA.items():
        with st.expander(f"✨ **Template: {name}**", icon="📋"):
            st.markdown(f"**👤 Persona:** {data['persona']}")
            st.markdown(f"**🏢 Context:** {data['context']}")
            st.markdown(f"**🎯 Task:** {data['task']}")
            st.markdown(f"**⚖️ Rules:**<br>{data['rules'].replace(chr(10), '<br>')}", unsafe_allow_html=True)
            st.markdown(f"**📋 Format:** {data['format']}")


# ══════════════════════════════════════════════════════════════
# TAB 3: SETUP GUIDE (Extremely Detailed, Boxed UI)
# ══════════════════════════════════════════════════════════════
with tabs[2]:
    st.write("### 📖 Sách Hướng Dẫn Kích Hoạt 100% Sức Mạnh AI")
    st.info("Đọc xong 3 bước dưới đây, bạn sẽ bỏ được thói quen xài AI sơ sài nhạt nhẽo như dùng Google Search.")
    
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
            st.markdown("**(3. Profile Team Kế Hoạch / Ideas / Marketing)**")
            st.code("""[Định Vị] Tôi là Marketing/Idea Planner chuyên target khách hàng Gen Z và Gen Alpha.
[Kỳ Vọng] Đừng bao giờ lặp lại lối mòn. Mình cần những góc nhìn điên rồ, lách luật (nhưng không vi phạm đạo đức).
[Cấm kỵ] CẤM viết văn phong hành chính, khô khan, giọng thông tấn xã. CẤM dùng lại các khuôn mẫu template quảng cáo có sẵn trên mạng.
[Format] Trình bày bài viết theo cấu trúc: 1. Hook (Từ khoá bắt tai) -> 2. Story (Kể chuyện) -> 3. Twist (Bất ngờ) -> CTA. Bắt buộc nhét Emoji cho sinh động.""", language="text")
            
            st.markdown("**(4. Profile Pháp Chế / Nhân Sự / Compliance)**")
            st.code("""[Định Vị] Tôi là Chuyên viên Pháp chế và Nhân sự Doanh nghiệp. 
[Kỳ Vọng] Mọi quyết định hay từ ngữ của bạn phải tuân thủ Luật Lao động VN và đảm bảo 0% rủi ro kiện tụng cho Tổ chức.
[Cấm kỵ] CẤM suy diễn luật hay áp dụng US Law vào VN. 
[Format] Giọng văn sắc lạnh, khách quan, không chứa cảm xúc cá nhân. Luôn luôn trích dẫn bằng Blockquote đoạn văn gốc nếu có thực hiện sửa đổi hợp đồng.""", language="text")

    st.markdown("<br>", unsafe_allow_html=True)
    
    # ------------- ÁP DỤNG MỆNH LỆNH XML -------------
    with st.container(border=True):
        st.subheader("⚙️ Bước 2: Gắn System Prompt chuẩn XML (Tạo Khung Hình Phạt)")
        st.markdown('''
        Khi bạn muốn AI KHÔNG ĐƯỢC bịa số liệu tài chính của phòng ban, bạn phải có Cấu Trúc Khối Lệnh Đóng Khung (Thẻ XML giống hệ thống ở Tab 1 của ứng dụng này).
        
        **Cách dùng khối lệnh XML khép kín:**
        1. Vào **Claude AI** $\\rightarrow$ Nhấn vào mục **Projects** ở cột menu bên trái $\\rightarrow$ Tạo một Project (Ví dụ: `Dự Án Báo Cáo Q3`).
        2. Dán toàn bộ khối lệnh gồm các thẻ ( `<persona>`, `<task>`, `<rules>`...) mà bạn copy ở Tab 1 vào cái ô **Project Instructions** to chà bá.
        3. 🚀 *Lợi ích khổng lồ:* Trọn đời ở trong cái Project đó, bạn chỉ cần tải file Excel Q3 lên rồi chat nắn gọn: *"Làm slide đi sếp"*. Claude AI sẽ tự ngầm hiểu kích hoạt 100% luật XML ẩn ở trên để xử lý nội dung cực chuyên, không sai 1 li nào.
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
        3. **Check Chéo:** Bạn tự rà soát lại 20 gạch đầu dòng đó. Cực kỳ uy tín vì NotebookLM có đính kèm trích xuất số `[1]` để bạn bấm vào là nó lật đúng trang sách gốc hiện lên rõ ràng minh chứng.
        4. **Xử Lý Chuyên Sâu Tinh Gọn:** Copy cái tóm lược "vàng" 20 gạch đầu dòng đó (Sạch sẽ, không rác) thả kéo về cho **Claude hoặc ChatGPT** $\\rightarrow$ Ra lệnh: *"Dựa vào Dữ kiện lõi đắt giá dưới đây, viết một Email Báo cáo Khẩn gửi Tổng Giám Đốc."*
        
        **Tổng Kết**: Làm 4 thao tác này giúp Tiết kiệm triệt để Token limit, AI xử lý siêu tốc 5 giây và nói KHÔNG với Dữ liệu Ma!
        ''')


# End of app
