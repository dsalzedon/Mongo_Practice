from flask import Flask, jsonify, request
from flask_restful import Api, Resource
from pymongo import MongoClient

app = Flask(__name__)
api = Api(app)


client = MongoClient("mongodb://db:27017")
# client = MongoClient("localhost", 27017)
db = client.newdb  # db
user_number = db.user_num  # collection
user_number.insert_one({"numbers_of_users": 0})


class Visit(Resource):
    """no docs"""

    def get(self):
        """no docs"""
        prev_num = user_number.find({})[0]["numbers_of_users"]
        new_number = prev_num + 1
        user_number.update_one({}, {"$set": {"numbers_of_users": new_number}})
        return str("Hello user " + str(new_number))


def check_posted_data(posted_data, function_name="default"):
    """missing docs"""
    missing_param_condition = "x" not in posted_data or "y" not in posted_data

    divide_condition = function_name == "divide"
    divide_by_zero_condition = posted_data["y"] == 0

    return (
        301
        if missing_param_condition or (divide_condition and divide_by_zero_condition)
        else 200
    )


class Add(Resource):
    """func"""

    def post(self):
        """func"""
        posted_data = request.get_json()

        status_code = check_posted_data(posted_data)

        if status_code != 200:
            return_json = {"message": "an error happened", "status code": status_code}
            return jsonify(return_json)

        x = int(posted_data["x"])
        y = int(posted_data["y"])
        calculation = x + y
        return_json = {"Calculation": calculation, "Status Code": status_code}
        return jsonify(return_json)


class Sub(Resource):
    """func"""

    def post(self):
        """func"""
        posted_data = request.get_json()

        status_code = check_posted_data(posted_data)

        if status_code != 200:
            return_json = {"message": "an error happened", "status code": status_code}
            return jsonify(return_json)

        x = int(posted_data["x"])
        y = int(posted_data["y"])
        calculation = x - y
        return_json = {"Calculation": calculation, "Status Code": status_code}
        return jsonify(return_json)


class Mult(Resource):
    """func mult"""

    def post(self):
        """func"""
        posted_data = request.get_json()
        status_code = check_posted_data(posted_data)

        if status_code != 200:
            return_json = {"message": "an error happened", "status code": status_code}
            return jsonify(return_json)

        x = int(posted_data["x"])
        y = int(posted_data["y"])
        calculation = x * y
        return_json = {"Calculation": calculation, "Status Code": status_code}
        return jsonify(return_json)


class Divide(Resource):
    """func"""

    def post(self):
        """func"""
        posted_data = request.get_json()

        status_code = check_posted_data(posted_data, "divide")

        if status_code != 200:
            return_json = {"message": "an error happened", "status code": status_code}
            return jsonify(return_json)

        x = int(posted_data["x"])
        y = int(posted_data["y"])
        calculation = x / y
        return_json = {"Calculation": calculation, "Status Code": status_code}
        return jsonify(return_json)


api.add_resource(Add, "/add")
api.add_resource(Sub, "/sub")
api.add_resource(Mult, "/mult")
api.add_resource(Divide, "/divide")
api.add_resource(Visit, "/hello")


if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)
