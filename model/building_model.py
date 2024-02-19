from model.db_connector import DBConnector
import mysql.connector

from utility.tool import replace_empty


def batch_building_insert(items, source_type):
    try:
        with DBConnector() as db:

            insert_detail_query_string = '''
                INSERT INTO Buildings (name, city, district, address, size_info, price, price_unit, source_type, source_id, status, room_info)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                ON DUPLICATE KEY UPDATE
                name = VALUES(name),
                city = VALUES(city),
                district = VALUES(district),
                address = VALUES(address),
                size_info = VALUES(size_info),
                price = VALUES(price),
                price_unit = VALUES(price_unit),
                source_type = VALUES(source_type),
                source_id = VALUES(source_id),
                status = VALUES(status),
                room_info = VALUES(room_info),
                update_datetime = NOW();
            '''

            detail_value = [
                (
                    replace_empty(item['name']),
                    replace_empty(item['city']),
                    replace_empty(item['district']),
                    replace_empty(item['address']),
                    replace_empty(item['size_info']),
                    replace_empty(item['price']),
                    replace_empty(item['price_unit']),
                    source_type,
                    replace_empty(item['source_id']),
                    item['status'],
                    replace_empty(item['room_info']),
                )
                for item in items
            ]

            db.execute_many_query(insert_detail_query_string, detail_value)

    except mysql.connector.Error as err:
        print(f"SQL Error: {err}")
        db.rollback()
    except Exception as e:
        print(f"Error: {e}")


def get_build_list_count(source_type):
    try:
        with DBConnector() as db:
            query_string = f'''
                SELECT
                    count(1) as total_count
                FROM Buildings 
                WHERE source_type = %s
            '''

            result = db.execute_query(query_string, [source_type])
            return result[0]
    except mysql.connector.Error as err:
        print(f"SQL Error: {err}")
    except Exception as e:
        print(f"Error: {e}")


def get_build_list(source_type, page=0):
    try:
        pageStart = page * 100

        with DBConnector() as db:
            query_string = f'''
                SELECT
                    building_id, source_id
                FROM Buildings 
                WHERE source_type = %s
                ORDER BY source_id
                LIMIT {pageStart}, 100
            '''

            result = db.execute_query(query_string, [source_type])
            print('sslls')
            return result
    except mysql.connector.Error as err:
        print(f"SQL Error: {err}")
    except Exception as e:
        print(f"Error: {e}")


def build_detail_transaction_insert(building_id, item_detail):
    with DBConnector() as db:
        try:
            db.start_transaction()
            insert_deatil_string = '''
                INSERT INTO BuildingItemDetail (
                building_id, build_type_name, is_upscale, purpose_name, purpose_other_name, deal_time, decorate,
                reception_address, park_price, base_area, base_area_unit, build_area, build_area_unit, terrace, terrace_unit, 
                down_pay, lend_rate, ratio, jbrate, park_ratio, park_planning, park_style, manage_cost, manage_cost_unit, 
                structural_engine, land_division, households, floor, build_intro, direction_rule, property_company, license, 
                use_license, width_deep, elevator_status_str, remark, latitude, longitude
            )
            VALUES (
                %s, %s, %s, %s, %s, %s, %s, %s, %s, %s,
                %s, %s, %s, %s, %s, %s, %s, %s, %s, %s,
                %s, %s, %s, %s, %s, %s, %s, %s, %s, %s,
                %s, %s, %s, %s, %s, %s, %s, %s
            )
            ON DUPLICATE KEY UPDATE
                build_type_name = VALUES(build_type_name),
                is_upscale = VALUES(is_upscale),
                purpose_name = VALUES(purpose_name),
                purpose_other_name = VALUES(purpose_other_name),
                deal_time = VALUES(deal_time),
                decorate = VALUES(decorate),
                reception_address = VALUES(reception_address),
                park_price = VALUES(park_price),
                base_area = VALUES(base_area),
                base_area_unit = VALUES(base_area_unit),
                build_area = VALUES(build_area),
                build_area_unit = VALUES(build_area_unit),
                terrace = VALUES(terrace),
                terrace_unit = VALUES(terrace_unit),
                down_pay = VALUES(down_pay),
                lend_rate = VALUES(lend_rate),
                ratio = VALUES(ratio),
                jbrate = VALUES(jbrate),
                park_ratio = VALUES(park_ratio),
                park_planning = VALUES(park_planning),
                park_style = VALUES(park_style),
                manage_cost = VALUES(manage_cost),
                manage_cost_unit = VALUES(manage_cost_unit),
                structural_engine = VALUES(structural_engine),
                land_division = VALUES(land_division),
                households = VALUES(households),
                floor = VALUES(floor),
                build_intro = VALUES(build_intro),
                direction_rule = VALUES(direction_rule),
                property_company = VALUES(property_company),
                license = VALUES(license),
                use_license = VALUES(use_license),
                width_deep = VALUES(width_deep),
                elevator_status_str = VALUES(elevator_status_str),
                latitude = VALUES(latitude),
                longitude = VALUES(longitude),
                remark = VALUES(remark);
            '''
            detail_value = [
                building_id, replace_empty(item_detail['build_type_name']),
                replace_empty(item_detail['is_upscale']),
                replace_empty(item_detail['purpose_name']),
                replace_empty(item_detail['purpose_other_name']),
                replace_empty(item_detail['deal_time']['date']),
                replace_empty(item_detail['decorate']),
                replace_empty(item_detail['reception_address']),
                replace_empty(item_detail['park_price']['price']),
                replace_empty(item_detail['base_area']['area']),
                replace_empty(item_detail['base_area']['unit']),
                replace_empty(item_detail['build_area']['area']),
                replace_empty(item_detail['build_area']['unit']),
                replace_empty(item_detail['terrace']['area']),
                replace_empty(item_detail['terrace']['unit']),
                replace_empty(item_detail['down_pay']),
                replace_empty(item_detail['lend_rate']),
                replace_empty(item_detail['ratio']),
                replace_empty(item_detail['jbrate']),
                replace_empty(item_detail['park_ratio']),
                replace_empty(item_detail['park_planning']),
                replace_empty(item_detail['park_style']),
                replace_empty(item_detail['manage_cost']['price']),
                replace_empty(item_detail['manage_cost']['unit']),
                replace_empty(item_detail['structural_engine']),
                replace_empty(item_detail['land_division']),
                replace_empty(item_detail['households']),
                replace_empty(item_detail['floor']),
                replace_empty(item_detail['build_intro']),
                replace_empty(item_detail['direction_rule']),
                replace_empty(item_detail['property_company']),
                replace_empty(item_detail['license']),
                replace_empty(item_detail['use_license']),
                replace_empty(item_detail['width_deep']),
                replace_empty(item_detail['elevator_status_str']),
                replace_empty(item_detail['remark']),
                replace_empty(item_detail['map']['lat']),
                replace_empty(item_detail['map']['lng']),
            ]

            insert_tag_string = '''
                INSERT INTO BuildingTag (building_id, tag_name)
                VALUES(%s, %s)
                ON DUPLICATE KEY UPDATE
                    update_datetime = NOW()
            '''
            tag_list = item_detail['label']
            tag_value = [(building_id, tag) for tag in tag_list]

            insert_facility_string = '''
                INSERT INTO BuildingFacility (building_id, facility_name)
                VALUES(%s, %s)
                ON DUPLICATE KEY UPDATE
                    update_datetime = NOW()
            '''

            facility_list = item_detail['facility']
            facility_value = [(building_id, facility)
                              for facility in facility_list]

            insert_traffic_string = '''
                INSERT INTO BuildingTraffic (building_id, traffic_type, content)
                VALUES(%s, %s, %s)
                ON DUPLICATE KEY UPDATE
                    update_datetime = NOW()
            '''
            traffic_list = item_detail['transportation']
            traffic_value = [
                (building_id, traffic['title'], traffic['content'])for traffic in traffic_list]

            insert_surround_string = '''
                INSERT INTO BuildingSurrounding (building_id, surround_type, content)
                VALUES(%s, %s, %s)
                ON DUPLICATE KEY UPDATE
                    update_datetime = NOW()
            '''
            surround_list = item_detail['surrounding']
            surround_value = [
                (building_id, surround['title'], surround['content'])for surround in surround_list]

            insert_design_string = '''
                INSERT INTO BuildingDesign (building_id, design_type, content)
                VALUES(%s, %s, %s)
                ON DUPLICATE KEY UPDATE
                    update_datetime = NOW()
            '''
            design_list = item_detail['building_design']
            design_value = [
                (building_id, design['title'], design['content'])for design in design_list]

            db.execute_query(insert_deatil_string, detail_value)
            db.execute_many_query(insert_tag_string, tag_value)
            db.execute_many_query(insert_facility_string, facility_value)
            db.execute_many_query(insert_traffic_string, traffic_value)
            db.execute_many_query(insert_surround_string, surround_value)
            db.execute_many_query(insert_design_string, design_value)

            db.commit()
        except mysql.connector.Error as err:
            print(f"SQL Error: {err}")
            db.rollback()
        except Exception as e:
            print(f"Error: {e}")


def batch_house_insert(items, source_type):
    try:
        with DBConnector() as db:

            insert_detail_query_string = '''
                INSERT INTO PreOwnedHouses (
                    name, purpose_name, shape_name, 
                    city, district, address, 
                    community_name, size_info, unit_price,
                    source_type, source_id, floor, room_info
                )
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                ON DUPLICATE KEY UPDATE
                    name = VALUES(name),
                    purpose_name = VALUE(purpose_name),
                    shape_name = VALUE(shape_name),
                    city = VALUES(city),
                    district = VALUES(district),
                    address = VALUES(address),
                    community_name = VALUE(community_name),
                    size_info = VALUES(size_info),
                    price = VALUES(price),
                    price_unit = VALUES(price_unit),
                    source_type = VALUES(source_type),
                    source_id = VALUES(source_id),
                    floor = VALUE(floor),
                    room_info = VALUE(room_info),
                    update_datetime = NOW();
            '''

            detail_value = [
                (
                    replace_empty(item['name']),
                    replace_empty(item['purpose_name']),
                    replace_empty(item['shape_name']),
                    replace_empty(item['city']),
                    replace_empty(item['district']),
                    replace_empty(item['address']),
                    replace_empty(item['community_name']),
                    replace_empty(item['size_info']),
                    replace_empty(item['unit_price']),
                    source_type,
                    replace_empty(item['source_id']),
                    replace_empty(item['floor']),
                    replace_empty(item['room_info']),
                    replace_empty(item['source_id'])
                )
                for item in items
            ]

            db.execute_many_query(insert_detail_query_string, detail_value)

    except mysql.connector.Error as err:
        print(f"SQL Error: {err}")
        db.rollback()
    except Exception as e:
        print(f"Error: {e}")
