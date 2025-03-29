import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.preprocessing import StandardScaler
import joblib
from mysite.settings import BASE_DIR


class ReportRecommendationModel:
    def __init__(self):
        self.df = None
        self.tfidf_vectorizer = None
        self.tfidf_matrix = None
        self.scaler = None

    def load_data(self, csv_path):
        """
        Загрузка и предобработка данных
        """
        self.df = pd.read_excel(csv_path)

        # Преобразование текстовых признаков
        self.df["text_features"] = self.df.apply(
            lambda row: f"{row['type_object']} {row['description']} {row['type_breaking']} {row['text_report']}",
            axis=1,
        )

        # Векторизация текста
        self.tfidf_vectorizer = TfidfVectorizer(stop_words=None)
        self.tfidf_matrix = self.tfidf_vectorizer.fit_transform(
            self.df["text_features"]
        )

        # Нормализация критериев качества
        quality_columns = ["diagnostic_data", "was_done", "result", "name_component"]
        self.scaler = StandardScaler()
        self.df["quality_score"] = self.scaler.fit_transform(
            self.df[quality_columns]
        ).sum(axis=1)

    def recommend_reports(self, type_object, description, type_breaking, top_n=3):
        """
        Рекомендация наиболее подходящих отчетов
        """
        # Создание входного вектора
        input_feature = f"{type_object} {description} {type_breaking}"
        input_vector = self.tfidf_vectorizer.transform([input_feature])

        # Вычисление косинусного сходства
        similarities = cosine_similarity(input_vector, self.tfidf_matrix)[0]

        # Фильтрация и ранжирование

        filtered_df = self.df[
            (self.df["type_object"] == type_object)
            & (self.df["quality_report"] != "Не подходит по критериям")
        ]

        filtered_df["similarity"] = similarities[filtered_df.index]
        filtered_df["final_score"] = (
            filtered_df["similarity"] * 0.6 + filtered_df["quality_score"] * 0.4
        )

        # Топ-3 рекомендации
        recommendations = filtered_df.nlargest(top_n, "final_score")

        return recommendations[["text_report", "final_score"]].to_dict("records")

    def save_model(self, path=f"{BASE_DIR}/model/report_recommendation_model.joblib"):
        """
        Сохранение модели для использования в PWA
        """
        model_data = {
            "tfidf_vectorizer": self.tfidf_vectorizer,
            "tfidf_matrix": self.tfidf_matrix,
            "scaler": self.scaler,
            "df": self.df,
        }
        joblib.dump(model_data, path)

    def load_model(self, path=f"{BASE_DIR}/model/report_recommendation_model.joblib"):
        """
        Загрузка предобученной модели
        """
        model_data = joblib.load(path)
        self.tfidf_vectorizer = model_data["tfidf_vectorizer"]
        self.tfidf_matrix = model_data["tfidf_matrix"]
        self.scaler = model_data["scaler"]
        self.df = model_data["df"]


# Функция для демонстрации и тестирования
def demonstrate_model(type_object, description, type_breaking):
    # Создание и обучение модели
    model = ReportRecommendationModel()
    model.load_data(f"{BASE_DIR}/model/parsed_dataset.xlsx")

    recommendations = model.recommend_reports(type_object, description, type_breaking)

    return recommendations
