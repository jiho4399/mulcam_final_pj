import os
from pickle import TRUE
import streamlit as st
# from multiapp import MultiApp
import pandas as pd
import numpy as np
import plotly.express as px
# from main import total_graph
from persist import persist, load_widget_state
from catboost_model import preprocessing, train_model, result
from catboost import CatBoostClassifier # 05/28
from io import BytesIO
from datetime import datetime
import streamlit_authenticator as stauth
import plotly.graph_objects as go
import altair as alt


st.set_page_config(layout = "wide")

st.markdown(
    """
    <style>
    [data-testid="stSidebar"][aria-expanded="true"] > div:first-child {
        width: 250px;
    }
    [data-testid="stSidebar"][aria-expanded="false"] > div:first-child {
        width: 250px;
        margin-left: -500px;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

def main():
    if "page" not in st.session_state:
        # Initialize session state.
        st.session_state.update({
            # Default page.
            "page": "home",

            # Radio, selectbox and multiselect options.
            "gender_options": ["여자", "남자"],

            # 기본값
            "text": "",
            "slider": 0,
            "checkbox": False,
            "radio": "F",
            "selectbox": "Hello",
            "multiselect": ["Hello", "Everyone"],
        })

    page = st.sidebar.radio("페이지를 선택해주세요.", tuple(PAGES.keys()), format_func=str.capitalize)
    st.header("마이데이터를 활용한 신용도 예측 시스템")
    PAGES[page]()

def login():
    names = '관리자'
    usernames = ['mulcam']
    passwords = ['123']
    hashed_passwords = stauth.Hasher(passwords).generate()
    authenticator = stauth.Authenticate(names,usernames,hashed_passwords,
    'some_cookie_name','some_signature_key',cookie_expiry_days=30)
    name, authentication_status, username = authenticator.login('Login','main')

    if authentication_status:
        column1, column2 = st.columns([1, 3])
        with column1:
            st.write('환영합니다. *%s* 님 ' % (names))
        with column2:
            authenticator.logout('Logout', 'main')
        st.write('Side bar에서 원하는 그래프 종류를 선택해주세요.')
        st.info('* 신용도는 0등급, 1등급, 2등급으로 분류되며 숫자가 낮을수록 신용도가 높습니다. \n\n * 전체 화면을 권장하며, 그래프 클릭하시면 더욱 자세히 볼 수 있습니다. \n\n * 그래프를 드래그하여 확대할 수 있으며 더블클릭 시 원래대로 돌아옵니다.')      
        PAGES2[st.sidebar.radio("기업전용 카테고리", tuple(PAGES2.keys()), format_func=str.capitalize)]()
    elif authentication_status == False:
        st.error('아이디나 비밀번호가 일치하지 않습니다.')
    elif authentication_status == None:
        st.warning('아이디와 비밀번호를 입력해주세요.')

# def column():
    # st.subheader('전체 표 보기: 신용도와 연관성')
    # # st.title('신용카드 사용자 신용도 예측 서비스')
    # DATA_PATH = ('./data/')

    # # 불러온 차트 보여주기
    # train = pd.read_csv(DATA_PATH + 'final_df.csv')
    # train.drop(['credit_r', 'DAYS_EMPLOYED'], axis=1, inplace=True)
    # test = pd.read_csv(DATA_PATH + 'final_test_df.csv')
    # test.drop(['DAYS_EMPLOYED'], axis=1, inplace=True)
    
    
    # column1, column2, column3 = st.columns(3)

    # with column1:

    #     #############
    #     pie_column=st.selectbox('1.선택한 항목과 유저수의 관계를 Pie chart로 나타냅니다.',
    #     ('gender','car', 'reality','work_phone','phone','email',
    #     'income_type', 'edu_type', 'family_type', 'house_type', 'occyp_type',
    #     'child_num','family_size'))
    #     if pie_column:
    #         for col in [pie_column]:
    #             df = train.copy()
    #             df = df.groupby(by=[col,'credit']).count().reset_index()
    #             df['credit'] = df['credit'].astype(str)
    #             fig = px.pie(df, width=400, height=400, values='Unnamed: 0', names=col, title=str('Pie chart: '+col), labels={col:'occyp_type','Unnamed: 0':'credit count'})
    #             st.plotly_chart(fig)

        
    #     income_column=st.selectbox('3. 선택한 항목과 income_total 평균의 관계를 나타냅니다.',
    #     ('gender', 'car', 'reality', 'income_type', 'edu_type', 'family_type', 'house_type', 'occyp_type','DAYS_BIRTH', 'family_size'))
    #     if income_column == 'DAYS_BIRTH' or income_column == 'family_size':
    #         for col1, col2 in [[income_column, 'income_total']]:
    #             df = train.copy()
    #             df = df.groupby([col1], as_index=False).mean()
    #             fig = px.line(df, x=col1, y=col2, title=str(col1+' 별 income_total 평균'), markers = True)
    #             st.plotly_chart(fig)
    #     else:
    #         for col1, col2 in [[income_column, 'income_total']]:
    #             df = train.copy()
    #             df = df.groupby([col1], as_index=False).mean()
    #             df = df.sort_values(by=[col2])
    #             fig = px.line(df,width=400, height=400, x=col1, y=col2, title=str(col1+' 별 income_total 평균'), markers = True)
    #             st.plotly_chart(fig)

    # with column2:
        
    #     income_column=st.selectbox('2. 선택한 항목과 income_total의 관계를 나타냅니다.',
    #     ('gender', 'car', 'reality', 'income_type', 'edu_type', 'family_type', 'house_type', 'occyp_type','DAYS_BIRTH', 'family_size'))
    #     for col1, col2 in [[income_column, 'income_total']]:
    #         df = train.copy()
    #         fig = px.box(df, width=400, height=400,x=col1, y=col2, title=str(col1+' 별 income_total 분포'))
    #         st.plotly_chart(fig)

        

    #     # 수정 필요
    #     bar_column1=st.selectbox('4.선택한 항목과  평균 연령의 관계를 Bar chart로 나타냅니다.',
    #     ('gender','car', 'reality','work_phone','phone','email',
    #     'income_type', 'edu_type', 'family_type', 'house_type', 'occyp_type',
    #     'child_num','family_size','begin_month','DAYS_BIRTH'))
    #     if bar_column1 == 'begin_month' or bar_column1 == 'DAYS_BIRTH' or bar_column1 == 'family_size' or bar_column1 == 'child_num':
    #         for col1, col2 in [[bar_column1, 'DAYS_EMPLOYED_r']]:
    #             df = train.copy()
    #             df = df.groupby([col1], as_index=False).mean()
    #             fig = px.line(df, width=400, height=400,x=col1, y=col2, title=str(col1+' 별 DAYS_EMPLOYED_r 평균 비율'), markers= True)
    #             st.plotly_chart(fig)
    #     elif bar_column1:
    #         for col1, col2 in [[bar_column1, 'DAYS_EMPLOYED_r']]:
    #             df = train.copy()
    #             df = df.groupby([col1], as_index=False).mean()
    #             df = df.sort_values(by=[col2])
    #             fig = px.line(df,width=400, height=400, x=col1, y=col2, title=str(col1+' 별 DAYS_EMPLOYED_r 평균 비율'), markers= True)
    #             st.plotly_chart(fig)
        
    # with column3:
    #     bar_column=st.selectbox('5.선택한 항목과 Credit의 관계를 Bar chart로 나타냅니다.',('income_type',
    #         'DAYS_BIRTH',
    #         'occyp_type',
    #         'begin_month',
    #         'edu_type',
    #         'family_type'))
    #     if bar_column:
    #         for col in [bar_column]:
    #             df = train.copy()
    #             df = df.groupby(by=[col,'credit']).count().reset_index()
    #             df['credit'] = df['credit'].astype(str)
    #             fig = px.bar(df,width=400, height=400, x=col, y="Unnamed: 0", title=str(col+' & credit count'), color="credit", labels={col:bar_column,'Unnamed: 0':'credit count'})
    #             st.plotly_chart(fig)
    #     # 수정 필요
    #     sb_column=st.selectbox('6.선택한 항목과 Credit의 관계를 Sunburst chart로 나타냅니다.',('income_type',
    #         'DAYS_BIRTH',
    #         'occyp_type',
    #         'begin_month',
    #         'edu_type'))
    #     if sb_column:
    #         for col in [sb_column]:
    #             df = train.copy()
    #             fig = px.sunburst(df, width=400, height=400,path=['credit',col], title = str('credit count'+' & '+col))
    #             fig.update_layout(margin=dict(t=50, l=50, r=50, b=50)).update_traces(texttemplate="%{label}<br>%{percentEntry:.2%}")
    #             st.plotly_chart(fig)

# 수정 필요
    # input_column=st.selectbox('4. 선택한 항목과 gender의 관계를 나타냅니다.',
    # ('income_type', 'edu_type', 'occyp_type', 'income_total'))
    # if input_column == 'income_total':
    #     for col1, col2 in [[input_column, 'gender']]:
    #         df = train.copy()
    #         fig = px.box(df, x=col2, y=col1, title=str(col1+' 별 gender의 분포'))
    #         st.plotly_chart(fig)
    # else:     
    #     for col1, col2 in [[input_column, 'gender']]:
    #         df = train.copy()
    #         fig = px.bar(df, x=col2, y=col1, title=str(col1+' 별 gender의 분포'))
    #         st.plotly_chart(fig)

# 수정 필요






    ###############


    # 주거 형태 별 가족 규모
    # for col1, col2 in [['house_type', 'family_size']]:
    #     df = train.copy()
    #     df = df.groupby([col1], as_index=False).mean()
    #     # df = df.sort_values(by=[col2])
    #     fig = px.line(df, x=col1, y=col2, title=str('주거 형태 별 가족 규모'), markers = True)
    #     st.plotly_chart(fig)    


    # #income_type
    # for col in ['income_type']:
    # # for col1, col2 in [['credit', 'income_type']]:
    #     df = train.copy()
    #     df = df.groupby(by=[col,'credit']).count().reset_index()
    #     df['credit'] = df['credit'].astype(str)
    #     # fig = px.sunburst(df, path=[col1,col2], title = str('Sun chart: '+col1+' & '+col2))
    #     fig = px.bar(df, x=col, y="Unnamed: 0", title=str('Bar chart: '+col+' & credit count'), color="credit", labels={col:'income_type','Unnamed: 0':'credit count'})
    #     st.plotly_chart(fig)

    # #days_birth
    # for col in ['DAYS_BIRTH']:
    #     df = train.copy()
    #     df = df.groupby(by=[col,'credit']).count().reset_index()
    #     df['credit'] = df['credit'].astype(str)
    #     fig = px.bar(df, x=col, y="Unnamed: 0", title=str('Bar chart: '+col+' & credit count'), color="credit", labels={col:'age','Unnamed: 0':'credit count'})
    #     st.plotly_chart(fig)

    # #DAYS_EMPLOYED
    # for col in ['DAYS_EMPLOYED_r']:
    #     df = train.copy()
    #     df = df[df['DAYS_EMPLOYED_r'] > 0]
    #     df = df.groupby(by=[col,'credit']).count().reset_index()
    #     df['credit'] = df['credit'].astype(str)
    #     fig = px.scatter(df, x=col, y="Unnamed: 0", title=str('scatter chart: '+col+' & credit count'), color="credit", labels={col:'DAYS_EMPLOYED_r','Unnamed: 0':'credit count'})
    #     fig.update_layout(legend_traceorder='reversed')
    #     st.plotly_chart(fig)

    # #occyp_type
    # # for col in ['occyp_type']:
    # #     df = train.copy()
    # #     df = df.groupby(by=[col,'credit']).count().reset_index()
    # #     df['credit'] = df['credit'].astype(str)
    # #     fig = px.pie(df, values='Unnamed: 0', names=col, title=str('Pie chart: '+col), labels={col:'occyp_type','Unnamed: 0':'credit count'})
    # #     # fig.show()
    # #     st.plotly_chart(fig)
    # for col1, col2 in [['credit','occyp_type']]:
    #     df = train.copy()
    #     fig = px.sunburst(df, path=[col1,col2], title = str('Sun chart: '+col1+' & '+col2))
    #     fig.update_layout(margin=dict(t=50, l=50, r=50, b=50)).update_traces(texttemplate="%{label}<br>%{percentEntry:.2%}")
    #     st.plotly_chart(fig)

    # #begin_month
    # for col in ['begin_month']:
    #     df = train.copy()
    #     df = df.groupby(by=[col,'credit']).count().reset_index()
    #     df['credit'] = df['credit'].astype(str)
    #     fig = px.bar(df, x=col, y="Unnamed: 0", title=str('Bar chart: '+col+' & credit count'), color="credit", labels={col:'begin_month','Unnamed: 0':'credit count'})
    #     # fig.show()
    #     st.plotly_chart(fig)

    
    # # sunburst chart
    # # col1, col2, col3 in 범주형 변수, 범주형 변수, 범주형 변수
    # for col1, col2 in [['credit','income_type']]:
    #     df = train.copy()
    #     fig = px.sunburst(df, path=[col1,col2], title = str('Sun chart: '+col1+' & '+col2))
    #     # fig.show() 
    #     fig.update_layout(margin=dict(t=50, l=50, r=50, b=50)).update_traces(texttemplate="%{label}<br>%{percentEntry:.2%}")
    #     st.plotly_chart(fig)
        
    # for col1, col2 in [['credit', 'family_type']]:
    #     df = train.copy()
    #     fig = px.sunburst(df, path=[col1,col2], title = str('Sun chart: '+col1+' & '+col2))
    #     # fig.show()
    #     fig.update_layout(margin=dict(t=50, l=50, r=50, b=50)).update_traces(texttemplate="%{label}<br>%{percentEntry:.2%}")
    #     st.plotly_chart(fig)
     
    #     # 데이터 전처리
    # train.drop('Unnamed: 0', axis=1, inplace=True)
    # # pre_train, pre_test = preprocessing(train, test)
    # train['ability'] = train['income_total'] / (train['DAYS_BIRTH']*365 + train['DAYS_EMPLOYED_r']*365)
    # train['income_mean'] = train['income_total'] / train['family_size']


    # #ability
    # for col1, col2 in [['ability', 'income_type']]:
    #     df = train.copy()
    #     df['credit'] = df['credit'].astype(str)
    #     fig = px.scatter(df, x=col2, y=col1, color="credit", title=str('Scatter chart: '+col1+' & '+col2))
    #     fig.update_layout(legend_traceorder='reversed')
    #     st.plotly_chart(fig)
    
    # #income_mean
    # for col1, col2 in [['income_mean', 'family_type']]:
    #     # df = train.copy()
    #     df['credit'] = df['credit'].astype(str)
    #     fig = px.scatter(df, x=col2, y=col1, color="credit", title=str('Scatter chart: '+col1+' & '+col2))
    #     fig.update_layout(legend_traceorder='reversed')
    #     st.plotly_chart(fig)
        


    # st.write(
    #     f"""
    #     Settings values
    #     ---------------
    #     - **Gender**: {st.session_state.gender}
    #     - **Slider**: `{st.session_state.slider}`
    #     - **Checkbox**: `{st.session_state.checkbox}`
    #     - **Radio**: {st.session_state.radio}
    #     - **Selectbox**: {st.session_state.selectbox}
    #     - **Multiselect**: {", ".join(st.session_state.multiselect)}
    #     """
    # )


    
def my_settings():
    st.subheader("소비자용 내 정보 입력")
    st.text("정보를 입력해주세요.")

    gender=st.radio('성별', st.session_state["gender_options"], key=persist("gender"))
    DAYS_BIRTH=st.text_input('나이', placeholder='숫자만 입력. 예) 20세 = 20', max_chars=3)
    try:
        int(DAYS_BIRTH) 
    except:
        st.warning("형식에 맞게 입력해 주세요.")
    edu_type=st.selectbox('학력',('중학교 졸업', '고등학교 졸업', '대학생', '대학교 졸업(학사)', '석사 이상'))
    income_total=st.text_input('소득 (만 단위)', placeholder='숫자만 입력(만 단위). 예) 4000만원 = 4000', max_chars=6)
    try:
        int(income_total)
    except:
        st.warning("형식에 맞게 입력해 주세요.")
    child_num=st.text_input('자녀 수', placeholder='숫자만 입력. 예) 2명 = 2', max_chars=1)
    try:
        int(child_num)
    except:
        st.warning("형식에 맞게 입력해 주세요.")
    DAYS_EMPLOYED_r=st.text_input('고용연수', placeholder='숫자만 입력(연 단위). 예) 5년 = 5', max_chars=2)
    try:
        int(DAYS_EMPLOYED_r)
    except:
        st.warning("형식에 맞게 입력해 주세요.")
    work_phone=st.radio('직장 전화',('있음','없음'))
    phone=st.radio('집 전화',('있음','없음'))
    email=st.radio('이메일',('있음','없음'))
    car=st.radio('자동차',('있음','없음'))
    reality=st.radio('부동산',('있음','없음'))
    income_type=st.selectbox('소득 형태',('근로자', '사업가', '연금수령자', '공무원', '학생'))
    family_type=st.selectbox('가족 형태',('미혼', '기혼', '사실혼', '이혼', '미망인'))
    house_type=st.selectbox('주거 형태',('주택조합 아파트', '주택 / 아파트', '시립 아파트', '사옥', '임대 아파트', '부모님과 거주'))
    occyp_type=st.selectbox('직업',('회계사', '청소부원', '요리사', '사무직', '운전기사', '인사직', '전문직',
        'IT직', '일용직 노동자', '제조업 노동자', '관리자', '의료인', '민간 서비스직', '부동산업자', '영업직', '비서', '경비원', '웨이터 / 바텐더', '무직'))

    family_size=st.text_input('가족 규모', placeholder='본인 포함, 숫자만 입력. 예) 3명 = 3', max_chars=2)
    try:
        int(family_size)
    except:
        st.warning("형식에 맞게 입력해 주세요.")
    begin_month=st.text_input('신용카드 유효기간 (MM/YY) ', placeholder='MM/YY', max_chars=5, help='본인이 소유하고 있는 신용 카드 중 유효기간이 제일 긴 카드 입력하세요. 신용카드가 없으면 00/00을 입력하세요.')


    # 제출 버튼
    is_submit = st.button("제출")


    if is_submit:
        try:
            if begin_month== '00/00':
                begin_month = 0
            else:
                begin_month=int(begin_month[-2:])*12+int(begin_month[:2])-(datetime.today().year%100*12+datetime.today().month)
        # except:
        #     st.error('정보를 입력해 주세요.')

            input_dict = dict(
                성별=gender,
                자동차=car,
                부동산=reality,
                자녀_수=child_num,
                소득=income_total,
                소득_형태=income_type,
                학력=edu_type,
                가족_형태=family_type,
                주거_형태=house_type,
                나이=DAYS_BIRTH,
                고용연수_r=DAYS_EMPLOYED_r,
                직장_전화=work_phone,
                집_전화=phone,
                이메일=email,
                직업=occyp_type,
                가족_규모=family_size,
                신용카드_유효기간=begin_month
            )

            filename = './data/input_list.csv'


            if not os.path.exists(filename):
                pd.DataFrame([], columns=input_dict.keys()).to_csv(filename, mode='w' ,header=True, index=False)
            a = pd.DataFrame([input_dict])
            a.to_csv(filename, mode='a', header=False, index=False)

            # 다른페이지로 이동
            # 결과 출력
            DATA_PATH = ('./data/')
            train = pd.read_csv(DATA_PATH + 'trans_final_df.csv')
            # train.drop(['Unnamed: 0', '신용도_r', '고용연수'], axis=1, inplace=True)
            train.drop(['고용연수'], axis=1, inplace=True)

            X_train = pd.read_csv(DATA_PATH + 'input_list.csv')

            preprocessing(train, X_train)
            from_file = CatBoostClassifier()  # 5/28
            from_file.load_model("./data/model.bin") # 5/28
            y_predict = from_file.predict(X_train) # 5/28

            # 모델 학습
            # model_cat, X_train = train_model(pre_train, pre_test)
            # model_cat.save_model("./data/model.bin") # 5/28

            your_score = y_predict[0][0]
            st.info(f"당신의 신용도는 \"{your_score}등급\"입니다.\n\n(신용도는 0등급, 1등급, 2등급으로 분류되며 숫자가 낮을수록 신용도가 높습니다.)")
        except:
            st.error('정보를 입력해 주세요.')

    # 초기화 버튼
    is_reset = st.button("초기화", )
    try:
        if is_reset:
            os.unlink('./data/input_list.csv')
            st.success('데이터가 초기화되었습니다.')
    except:
        st.error('데이터가 없습니다.')

def my_graph():
    # st.header("마이데이터를 활용한 신용도 예측 시스템")
    st.subheader("내 표 보기")

def family(df):
    df['가족_규모']=df['가족_규모'].replace(1,'1명')
    df['가족_규모']=df['가족_규모'].replace(2,'2명')
    df['가족_규모']=df['가족_규모'].replace(3,'3명')
    df['가족_규모']=df['가족_규모'].replace(4,'4명')
    df['가족_규모']=df['가족_규모'].replace(5,'5명')
    df['가족_규모']=df['가족_규모'].replace(6,'6명')
    df['가족_규모']=df['가족_규모'].replace(7,'7명')

DATA_PATH = ('./data/')
train = pd.read_csv(DATA_PATH + 'trans_final_df.csv')

def credit_graph():

    st.subheader('신용도와 연관된 전체 표 보기')


    # st.text('*신용도는 0등급, 1등급, 2등급으로 분류되며 숫자가 낮을수록 신용도가 높습니다.')
    # st.text('*전체 화면을 권장하며, 신용도를 클릭하시면 더욱 자세히 볼 수 있습니다.')
    # st.title('신용카드 사용자 신용도 예측 서비스')
    # DATA_PATH = ('./data/')

    # # 불러온 차트 보여주기
    # train = pd.read_csv(DATA_PATH + 'trans_final_df.csv')
    # train.drop(['credit_r', 'DAYS_EMPLOYED'], axis=1, inplace=True)
    # test = pd.read_csv(DATA_PATH + 'final_test_df.csv')
    # test.drop(['DAYS_EMPLOYED'], axis=1, inplace=True)
    
    
    # column1, column2, column3 = st.columns(3)
    column1, column2 = st.columns(2)

    with column1:
        # 수정 필요
        # sb_column=st.selectbox('6.선택한 항목과 Credit의 관계를 Sunburst chart로 나타냅니다.',('income_type',
        #     'DAYS_BIRTH',
        #     'occyp_type',
        #     'begin_month',
        #     'edu_type'))
        # for col in ['소득_형태','성별','연령대','소득_4분위']:
        for col in ['소득_형태','가족_규모','소득_5분위']:
            df = train.copy()
            # df['소득 4분위']=df['소득 4분위'].astype('int64')
            fig = px.sunburst(df,width=600, height=600,color_discrete_sequence=px.colors.qualitative.Pastel1, path=['신용도',col], title = str(col+'별 신용도 비율'))
            fig.update_layout(margin=dict(t=80)).update_traces(texttemplate="%{label}<br>%{percentEntry:.2%}",)
            st.plotly_chart(fig)


    with column2:
        for col in ['성별','연령대','소득_10분위']:
            df = train.copy()
            # df['소득 5분위']=df['소득 5분위'].astype('int64')
            family(df)
            fig = px.sunburst(df, width=600, height=600,color_discrete_sequence=px.colors.qualitative.Pastel1,path=['신용도',col], title = str(col+'별 신용도 비율'))
            fig.update_layout(margin=dict(t=80)).update_traces(texttemplate="%{label}<br>%{percentEntry:.2%}")
            st.plotly_chart(fig)
            
    col1, col2 = st.columns([3,1])
    # with col1:
        #income_type
    with col1:
        for col in ['학력']:
            df = train.copy()
            df = df.groupby(by=[col,'신용도']).count().reset_index()
            df['신용도'] = df['신용도'].astype(str)
            df = df.sort_values(by=["Unnamed: 0"])
            fig = px.bar(df, width=900, height=600,x=col, y="Unnamed: 0",title=str('학력별 신용도 수'),color_discrete_sequence=['rgb(179, 205, 227)','rgb(141, 211, 199)','lightpink',],barmode='group',color="신용도", labels={col:'학력','Unnamed: 0':'인원'})
            fig.add_annotation(text="신용도 0일수록 신용도가 높음. 2가 제일 낮음",
                        xref="paper", yref="paper",
                        x=0.99, y=0.99, showarrow=False)
            st.plotly_chart(fig)
    

        for col in ['직업']:
            df = train.copy()
            df = df.groupby(by=[col,'신용도']).count().reset_index()
            df['신용도'] = df['신용도'].astype(str)
            df = df.sort_values(by=["Unnamed: 0"])
            fig = px.bar(df, width=900, height=600,x=col, y="Unnamed: 0",title=str('직업별 신용도 수'),color_discrete_sequence=['rgb(179, 205, 227)','rgb(141, 211, 199)','lightpink',],barmode='group',color="신용도", labels={col:'직업_유형','Unnamed: 0':'인원'})
            fig.add_annotation(text="신용도 0일수록 신용도가 높음. 2가 제일 낮음",
                        xref="paper", yref="paper",
                        x=0.99, y=0.99, showarrow=False)
            st.plotly_chart(fig)

    with col2:
        for col in ['학력']:
            df = train.copy()
            df = pd.pivot_table(df, index='학력', columns='신용도', values='소득', aggfunc='count')
            df.rename(columns = {0 : '신용도0'}, inplace = True)
            df.rename(columns = {1 : '신용도1'}, inplace = True)
            df.rename(columns = {2 : '신용도2'}, inplace = True)
            fig = go.Figure(data=[go.Table(
                header=dict(
                values=['학력','0 등급','1 등급','2 등급'],
                            fill_color='paleturquoise',
                            align='left'),
                cells=dict(values=[df.index, df.신용도0, df.신용도1, df.신용도2],fill_color='lavender',align='left'))])
            fig.update_layout(width=400, height=600,margin = dict(t=240, l=0, r=100, b=50))
            # width=900,height=500
            st.plotly_chart(fig)

        for col in ['직업']:
            df = train.copy()
            df = pd.pivot_table(df, index='직업', columns='신용도', values='소득', aggfunc='count')
            df.rename(columns = {0 : '신용도0'}, inplace = True)
            df.rename(columns = {1 : '신용도1'}, inplace = True)
            df.rename(columns = {2 : '신용도2'}, inplace = True)
            fig = go.Figure(data=[go.Table(
                header=dict(
                values=['직업','0 등급','1 등급','2 등급'],
                            fill_color='paleturquoise',
                            align='left'),
                cells=dict(values=[df.index, df.신용도0, df.신용도1, df.신용도2],fill_color='lavender',align='left'))])
            fig.update_layout(width=400, height=600,margin = dict(t=50, l=0, r=100, b=50))
            # width=900,height=500
            st.plotly_chart(fig)


    # with col2:
    #     pass

            # df = train.copy()
            # # df['소득 5분위']=df['소득 5분위'].astype('int64')
            # fig = px.sunburst(df, width=600, height=600,path=['신용도',col], title = str(col+'별 신용도 비율'))
            # fig.update_layout(margin=dict(t=80)).update_traces(texttemplate="%{label}<br>%{percentEntry:.2%}")
            # st.plotly_chart(fig)
            # x=col, y='신용도'

    # with column3:
    #         df = train.copy()
    #         fig = px.sunburst(df, width=450, height=450,path=['신용도','성별'], title = str('성별 신용도 비율'))
    #         fig.update_layout(margin=dict(t=80)).update_traces(texttemplate="%{label}<br>%{percentEntry:.2%}")
    #         st.plotly_chart(fig)

    #     # for col in [sb_column]:
    #         df = train.copy()
    #         family(df)
            
    #         fig = px.sunburst(df, width=450, height=450,path=['신용도','가족 규모'], title = str('가족 규모별 신용도 비율'))
    #         fig.update_layout(margin=dict(t=80)).update_traces(texttemplate="%{label}<br>%{percentEntry:.2%}")
    #         st.plotly_chart(fig)  

    #         df = train.copy()            
    #         # df['소득 10분위']=df['소득 10분위'].astype('int64')
    #         fig = px.sunburst(df, width=450, height=450,path=['신용도','소득 10분위'], title = str('소득 10분위별 신용도 비율'))
    #         fig.update_layout(margin=dict(t=80)).update_traces(texttemplate="%{label}<br>%{percentEntry:.2%}")
    #         st.plotly_chart(fig)  

    # fig =go.Figure(go.Sunburst(df,
    #     labels=list(df['가족 규모']),
    #     parents=list(df['신용도']),
    #     values=list(df['Unnamed: 0']),
    # ))
    # # Update layout for tight margin
    # # See https://plotly.com/python/creating-and-updating-figures/
    # fig.update_layout(margin = dict(t=0, l=0, r=0, b=0))
    # st.plotly_chart(fig)  


    # --------------신용도 그래프 끝------------------   

def another_graph():      
    st.subheader('선택해서 표 보기')
    st.text('* 신용도와 관련이 깊은 요인을 분석합니다.')
    column1,column2=st.columns(2)
    with column1:
        income_column=st.selectbox('1. 선택한 항목별 연 소득의 분포를 상자 그림으로 나타냅니다.',('직업','성별', '자동차', '부동산', '소득_형태', '학력', '가족_형태', '주거_형태', '연령대',  '가족_규모'))
        for col1, col2 in [[income_column, '소득']]:
            df = train.copy()
            family(df)
            if col1 == '연령대':
                df = df.sort_values(by=["연령대"])
            elif col1 == '가족_규모':
                df = df.sort_values(by=["가족_규모"])
            fig = px.box(df, x=col1, y=col2, color_discrete_sequence=px.colors.qualitative.Pastel1, title=str(col1+' 별 연 소득 분포'))
            st.plotly_chart(fig)
            # 수정 필요

        income_column=st.selectbox('3. 선택한 항목별 고용연수의 분포를 상자 그림으로 나타냅니다.',('소득_10분위', '학력', '연령대',  '직업'))
        for col1, col2 in [[income_column, '고용연수']]:
            df = train.copy()
            family(df)
            if col1 == '연령대':
                df = df.sort_values(by=["연령대"])
            fig = px.box(df, x=col1, y=col2, color_discrete_sequence=px.colors.qualitative.Pastel1, title=str(col1+' 별 고용연수 분포'))
            st.plotly_chart(fig)

    with column2:
        income_column=st.selectbox('2. 선택한 항목과 연 소득 평균의 관계를 막대그래프로 나타냅니다.',('연령대', '성별', '자동차', '부동산', '소득_형태', '학력', '가족_형태', '주거_형태', '직업', '가족_규모'))
        if income_column == '가족_규모' or income_column == '연령대':
            for col1, col2 in [[income_column, '소득']]:
                df = train.copy()
                family(df)
                df = df.groupby([col1], as_index=False).mean()
                fig = px.bar(df, x=col1, y=col2, color_discrete_sequence=['rgb(141, 211, 199)'], title=str(col1+' 별 연 소득 평균'))
                st.plotly_chart(fig)
        else:
            for col1, col2 in [[income_column, '소득']]:
                df = train.copy()
                family(df)
                df = df.groupby([col1], as_index=False).mean()
                df = df.sort_values(by=[col2])
                fig = px.bar(df,x=col1, y=col2, color_discrete_sequence=['rgb(141, 211, 199)'], title=str(col1+' 별 연 소득 평균'))
            st.plotly_chart(fig)

        
        bar_column1=st.selectbox('4.선택한 항목과  고용연수 평균의 관계를 막대그래프로 나타냅니다.',
        ('소득_형태', '직업', '성별','자동차', '부동산',
         '학력', '가족_형태', '주거_형태', '가족_규모', '연령대'))
        if bar_column1 == '연령대' or bar_column1 == '가족_규모':
            for col1, col2 in [[bar_column1, '고용연수']]:
                df = train.copy()
                family(df)
                df = df.groupby([col1], as_index=False).mean()
                fig = px.bar(df, x=col1, y=col2, color_discrete_sequence=['rgb(179, 205, 227)'], title=str(col1+' 별 고용연수 평균 비율'))
                st.plotly_chart(fig)
        elif bar_column1:
            for col1, col2 in [[bar_column1, '고용연수']]:
                df = train.copy()
                df = df.groupby([col1], as_index=False).mean()
                df = df.sort_values(by=[col2])
                fig = px.bar(df,x=col1, y=col2, color_discrete_sequence=['rgb(179, 205, 227)'], title=str(col1+' 별 고용연수 평균 비율'))
                st.plotly_chart(fig)
        


    
    # bar_column=st.selectbox('5.선택한 항목과 Credit의 관계를 Bar chart로 나타냅니다.',('income_type',
    #     'DAYS_BIRTH',
    #     'occyp_type',
    #     'begin_month',
    #     'edu_type',
    #     'family_type'))
    # if bar_column:
    #     for col in [bar_column]:
    #         df = train.copy()
    #         df = df.groupby(by=[col,'credit']).count().reset_index()
    #         df['credit'] = df['credit'].astype(str)
    #         fig = px.bar(df,x=col, y="Unnamed: 0", title=str(col+' & credit count'), color="credit", labels={col:bar_column,'Unnamed: 0':'credit count'})
    #         st.plotly_chart(fig)

            #############
    # pie_column=st.selectbox('4.선택한 항목의 유저수를 원형 그래프로 나타냅니다.',
    # ('성별','자동차', '부동산','직장 전화','집 전화','이메일',
    # '소득 형태', '학력', '가족 형태', '주거 형태', '직업',
    # '아이 수','가족 규모'))
    # st.markdown('\n')
    # st.markdown('\n')
    # st.markdown('\n')
    # st.markdown('\n')
    # st.markdown('\n')
    # st.markdown('\n')
    # if pie_column:
def full_scale():
    st.subheader('전체 데이터 분포')
    column1,column2,column3,column4,column5,column6=st.columns(6)
    with column1:
        for col in ['신용도','직업']:
            df = train.copy()
            df = df.groupby(by=[col]).count().reset_index()
            family(df)
            df['신용도']=df['신용도'].astype(str)
            df = df.sort_values(by=["Unnamed: 0"])
            fig = px.bar(df, width=270, x=col, y="Unnamed: 0",color=col,color_discrete_sequence=px.colors.qualitative.Pastel2,labels={col:'','Unnamed: 0':'인원'})
            fig.update_layout(
                title={
                    'text': str(col+' 비율'),
                    'y':0.9,
                    'x':0.5,
                    'xanchor': 'center',
                    'yanchor': 'top'},
                showlegend=False,
            )
            st.plotly_chart(fig)
    with column2:
        for col in ['학력','소득_형태']:
            df = train.copy()
            df = df.groupby(by=[col]).count().reset_index()
            family(df)
            df['가족_규모']=df['가족_규모'].astype(str)
            df = df.sort_values(by=["Unnamed: 0"])
            fig = px.bar(df,width=270, x=col, y="Unnamed: 0", color=col,color_discrete_sequence=px.colors.qualitative.Pastel1,labels={col:'','Unnamed: 0':''})
            fig.update_layout(
                title={
                    'text': str(col+' 비율'),
                    'y':0.9,
                    'x':0.5,
                    'xanchor': 'center',
                    'yanchor': 'top'},
                showlegend=False)           
            st.plotly_chart(fig,showlegend="false")
    with column3:
        for col in ['주거_형태','가족_형태']:
            df = train.copy()
            df = df.groupby(by=[col]).count().reset_index()
            family(df)
            df = df.sort_values(by=["Unnamed: 0"])
            fig = px.bar(df,width=270, x=col, y="Unnamed: 0",color=col, color_discrete_sequence=px.colors.qualitative.Pastel1,labels={col:'','Unnamed: 0':''})
            fig.update_layout(
                title={
                    'text': str(col+' 비율'),
                    'y':0.9,
                    'x':0.5,
                    'xanchor': 'center',
                    'yanchor': 'top'},
                showlegend=False,)
            st.plotly_chart(fig,showlegend="false")
    with column4:
        for col in ['가족_규모', '자녀_수']:
            df = train.copy()
            df = df.groupby(by=[col]).count().reset_index()
            family(df)
            df['자녀_수']=df['자녀_수'].astype(str)
            # df = df.sort_values(by=["Unnamed: 0"])
            fig = px.bar(df,width=270, x=col, y="Unnamed: 0",color=col,color_discrete_sequence=px.colors.qualitative.Pastel1,labels={col:'','Unnamed: 0':''})
            fig.update_layout(
                title={
                    'text': str(col+' 비율'),
                    'y':0.9,
                    'x':0.5,
                    'xanchor': 'center',
                    'yanchor': 'top'},
                    showlegend=False,)

            st.plotly_chart(fig,showlegend="false")


    with column5:
        for col in ['성별', '연령대']:
            df = train.copy()
            df = df.groupby(by=[col]).count().reset_index()
            family(df)
            # df = df.sort_values(by=["Unnamed: 0"])
            fig = px.bar(df,width=270, x=col, y="Unnamed: 0", color=col,color_discrete_sequence=px.colors.qualitative.Pastel1,labels={col:'','Unnamed: 0':''})
            fig.update_layout(
                title={
                    'text': str(col+' 비율'),
                    'y':0.9,
                    'x':0.5,
                    'xanchor': 'center',
                    'yanchor': 'top'},
                showlegend=False,)

            st.plotly_chart(fig,showlegend="false")
    with column6:
        for col in ['자동차', '부동산']:
            df = train.copy()
            df = df.groupby(by=[col]).count().reset_index()
            family(df)
            df = df.sort_values(by=["Unnamed: 0"])
            df['자녀_수']=df['자녀_수'].astype(str)
            fig = px.bar(df,width=270, x=col, y="Unnamed: 0",color=col,color_discrete_sequence=px.colors.qualitative.Pastel1,labels={col:'','Unnamed: 0':''},
            )
            fig.update_layout(
                title={
                    'text': str(col+' 비율'),
                    'y':0.9,
                    'x':0.5,
                    'xanchor': 'center',
                    'yanchor': 'top'},
                showlegend=False,)
            st.plotly_chart(fig,showlegend="false")
        # labels={col:col,'Unnamed: 0':'유저 수'})
    # col=['성별','자동차', '부동산','직장 전화','집 전화','이메일',
    # '소득 형태', '학력', '가족 형태', '주거 형태', '직업',
    # '아이 수','가족 규모']
    # df = train.copy()
    # # df = df.groupby(by=[col,'credit']).count().reset_index()
    # # df['credit'] = df['credit'].astype(str)
    # fig = px.bar(df, x=col, y="Unnamed: 0", title=str('Bar chart: '+col+' & count'),labels={col:col,'Unnamed: 0':'count'})
    # # fig.show()
    # st.plotly_chart(fig)    
    # df = train.copy()
    # df = df.groupby(by=['성별']).count().reset_index()
    # trace_F=go.Bar(x=['성별'],y=df['성별'].count())
    # trace_M=go.Bar(x=df[df['성별']=='남성'],y=df[df['성별']=='남성'].count())
    # data=[trace_F,trace_M]
    # layout=go.Layout(title='성별 비율',barmode='stack')
    # fig=go.Figure(data=trace_F,layout=layout)
    # st.plotly_chart(fig)
    # bar_chart = alt.Chart(df).mark_bar().encode(
    #     y='Unnamed: 0',
    #     x="성별",
    # )
    # st.altair_chart(bar_chart, use_container_width=True)

PAGES = {
    "소비자용 내 정보 입력": my_settings,
    "기업용 전체 표 보기": login,
    # "내 표 보기" : my_graph

}

PAGES2 = {
    "전체 데이터 분포":full_scale,
    "신용도 그래프":credit_graph,
    "항목 선택 그래프":another_graph,
}
if __name__ == "__main__":
    load_widget_state()
    main()