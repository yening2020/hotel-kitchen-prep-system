from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required
from ...models.db import db
from ...utils.hotel_utils import utils_get_hotel_schema
from sqlalchemy import text

kitchen_prep_bp = Blueprint('kitchen_prep', __name__)

@kitchen_prep_bp.route("/<int:hotel_id>/preparations", methods=["GET"])
@jwt_required()
def get_preparations(hotel_id):
    """获取厨房准备任务列表"""
    try:
        schema = utils_get_hotel_schema(hotel_id)
        table_name = f"{schema}.kitchen_preparations" if schema else "kitchen_preparations"
        
        sql_query = text(f"""
            SELECT 
                id, 
                event_name,
                event_date,
                CAST(event_time AS VARCHAR(5)) AS event_time,
                guest_count,
                status, 
                progress
            FROM {table_name}
            ORDER BY event_date DESC, event_time DESC;
        """)

        result = db.session.execute(sql_query).fetchall()
        
        preparations_data = []
        for row in result:
            preparation = {
                'id': row.id,
                'event_name': row.event_name,
                'event_date': row.event_date.strftime('%Y-%m-%d') if row.event_date else None,
                'event_time': row.event_time,
                'guest_count': row.guest_count,
                'status': row.status,
                'progress': row.progress
            }
            preparations_data.append(preparation)

        return jsonify({
            "message": "成功获取厨房准备任务列表",
            "preparations": preparations_data
        }), 200

    except Exception as e:
        return jsonify({
            "message": f"无法处理获取厨房准备任务的请求 (hotel_id={hotel_id})",
            "preparations": []
        }), 500

@kitchen_prep_bp.route("/<int:hotel_id>/preparations/<int:preparation_id>", methods=["GET"])
@jwt_required()
def get_preparation_detail(hotel_id, preparation_id):
    """获取单个厨房准备任务的详细信息"""
    try:
        schema = utils_get_hotel_schema(hotel_id)
        base_table_name = f"{schema}.kitchen_preparations" if schema else "kitchen_preparations"
        items_table_name = f"{schema}.kitchen_preparation_items" if schema else "kitchen_preparation_items"
        requirements_table_name = f"{schema}.ingredient_requirements" if schema else "ingredient_requirements"

        # 获取主要准备任务信息
        main_query = text(f"""
            SELECT 
                id, 
                event_name,
                event_date,
                CAST(event_time AS VARCHAR(5)) AS event_time,
                guest_count,
                status,
                progress,
                notes,
                created_at,
                updated_at
            FROM {base_table_name}
            WHERE id = :prep_id
        """)
        
        # 获取准备项目信息
        items_query = text(f"""
            SELECT 
                kpi.id,
                kpi.preparation_id,
                kpi.dish_id,
                kpi.quantity,
                kpi.status,
                kpi.notes,
                d.name as dish_name,
                d.category as dish_category
            FROM {items_table_name} kpi
            LEFT JOIN dishes d ON kpi.dish_id = d.id
            WHERE kpi.preparation_id = :prep_id
        """)
        
        # 获取食材需求信息
        requirements_query = text(f"""
            SELECT 
                ir.id,
                ir.preparation_item_id,
                ir.ingredient_id,
                ir.required_amount,
                ir.unit,
                ir.status,
                i.name as ingredient_name,
                i.category as ingredient_category
            FROM {requirements_table_name} ir
            LEFT JOIN ingredients i ON ir.ingredient_id = i.id
            WHERE ir.preparation_item_id IN (
                SELECT id FROM {items_table_name}
                WHERE preparation_id = :prep_id
            )
        """)

        # 执行查询
        main_result = db.session.execute(main_query, {'prep_id': preparation_id}).fetchone()
        items_result = db.session.execute(items_query, {'prep_id': preparation_id}).fetchall()
        requirements_result = db.session.execute(requirements_query, {'prep_id': preparation_id}).fetchall()

        if not main_result:
            return jsonify({
                "message": f"未找到指定的厨房准备任务 (id={preparation_id})",
                "preparation": None
            }), 404

        # 构建响应数据
        preparation_items = []
        for item in items_result:
            preparation_items.append({
                'id': item.id,
                'preparation_id': item.preparation_id,
                'dish_id': item.dish_id,
                'dish_name': item.dish_name,
                'dish_category': item.dish_category,
                'quantity': item.quantity,
                'status': item.status,
                'notes': item.notes
            })

        ingredient_requirements = []
        for req in requirements_result:
            ingredient_requirements.append({
                'id': req.id,
                'preparation_item_id': req.preparation_item_id,
                'ingredient_id': req.ingredient_id,
                'ingredient_name': req.ingredient_name,
                'ingredient_category': req.ingredient_category,
                'required_amount': float(req.required_amount) if req.required_amount else 0,
                'unit': req.unit,
                'status': req.status
            })

        preparation_detail = {
            'id': main_result.id,
            'event_name': main_result.event_name,
            'event_date': main_result.event_date.strftime('%Y-%m-%d') if main_result.event_date else None,
            'event_time': main_result.event_time,
            'guest_count': main_result.guest_count,
            'status': main_result.status,
            'progress': main_result.progress,
            'notes': main_result.notes,
            'created_at': main_result.created_at.isoformat() if main_result.created_at else None,
            'updated_at': main_result.updated_at.isoformat() if main_result.updated_at else None,
            'preparation_items': preparation_items,
            'ingredient_requirements': ingredient_requirements
        }

        return jsonify({
            "message": "成功获取厨房准备任务详情",
            "preparation": preparation_detail
        }), 200

    except Exception as e:
        return jsonify({
            "message": f"获取厨房准备任务详情时发生错误: {str(e)}",
            "preparation": None
        }), 500