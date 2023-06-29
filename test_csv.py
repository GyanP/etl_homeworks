import csv
from pycountry_convert import country_name_to_country_alpha3
from decimal import Decimal, InvalidOperation


def read_csv(file_name):
    data = []
    with open(file_name, 'r', newline='') as file:
        reader = csv.reader(file)
        for row in reader:
            data.append(row)
    return data


def write_csv(file_name, data, headers):
    with open(file_name, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(headers)
        writer.writerows(data)


def format_currency(amount_str):
    try:
        amount = round(Decimal(amount_str), 2)
        return f"${amount}"
    except (ValueError, TypeError, InvalidOperation):
        return amount_str


def get_country_alpha3(country_name):
    try:
        alpha3_code = country_name_to_country_alpha3(country_name)
        return alpha3_code
    except:
        return None


def convert_to_inches(cell_value, header_value):
    unit_mappings = {
        "in": 1,
        "inches": 1,
        "cm": 0.393701,
        "centimeters": 0.393701,
    }

    try:
        value = float(cell_value)
        for unit in unit_mappings:
            if unit in cell_value.lower() or unit in header_value.lower():
                # Convert from centimeters to inches
                return round(value * unit_mappings[unit],1)
        return round(value, 1) if value else ''  # # Assume inches if no unit is specified
    except (ValueError, TypeError):
        return cell_value


def convert_to_pounds(cell_value, header_value):
    unit_mappings = {
        "lb": 1,
        "pound": 1,
        "kg": 2.20462,
        "kilogram": 2.20462,
    }

    try:
        value = float(cell_value)
        for unit in unit_mappings:
            if unit in cell_value.lower() or unit in header_value.lower():
                return round(value * unit_mappings[unit],1)
        return round(value, 1)  # Assume pounds if no unit is specified
    except (ValueError, TypeError):
        return cell_value


def convert_to_ean13(value):
    try:
        return f"0{value[0:2]}-{value[2:-1]}-{value[-1]}"
    except:
        return None


def is_prop_65_items(url_california_label_jpg, url_california_label_pdf):
    return True if "65" in url_california_label_jpg or "65" in url_california_label_pdf else False


def get_attrib__seat_depth(value):
    try:
        return value.split("x")[1]
    except (IndexError, AttributeError):
        return value


def get_attrib__seat_width(value):
    try:
        return value.split("x")[0]
    except (IndexError, AttributeError):
        return value
    
def get_cost_price(value):
    format_value = value.replace('$','') if isinstance(value, str) and value.find('$') == 0 else value
    try:
        # here I am assuming the profile percentage is 10%
        profit_percentage = 10
        value = float(format_value)
        cost_price = value / (1 + (profit_percentage / 100))
        cost_price = round(cost_price, 2)
        return cost_price
    except (AttributeError, TypeError, ValueError):
        return value


def main():
    # Read headers from example.csv
    headers = read_csv('example.csv')[0]

    # Read rows from homework.csv
    data = read_csv('homework.csv')
    new_data = []
    # Format cells according to industry standards
    for i in range(1, len(data)):  # Start from index 1 to skip the header row
        data[i] = [
            # manufacturer_sku
            data[i][0],
            # convert upc to ean13 format
            convert_to_ean13(data[i][1]),
            # check header and cell then convert weight into ponds if not in ponds
            convert_to_pounds(data[i][19], data[0][19]),
            # check header and cell value  convert length into inches if not in inches
            # length can be consider to item depth (inches)
            convert_to_inches(data[i][16], data[0][16]),
            # check header and cell value  convert width into inches if not in inches
            convert_to_inches(data[i][15], data[0][15]),
            # check header and cell value  convert height into inches if not in inches
            convert_to_inches(data[i][17], data[0][17]),
            # check the item is prop 65 or not
            is_prop_65_items(data[i][49], data[i][50]),
            # calculating the cost_price from wholesale price and assuming profit 10 %
            get_cost_price(data[i][6]),
            # min_price is not there also unable to calculate the min price ,
            None,
            # made_to_order is not available so by default store False,
            False,
            # item category
            data[i][12],
            # product brand name
            data[i][11],
            # title or short description of product
            data[i][9],
            # product__description or long description
            data[i][10],
            # selling point 1 or product__bullets__0
            data[i][135],
            # selling point 2 or product__bullets__1
            data[i][136],
            # selling point 3 or product__bullets__2
            data[i][137],
            # selling point 4 or product__bullets__3
            data[i][138],
            # selling point 5 or product__bullets__4
            data[i][139],
            # selling point 6 or product__bullets__5
            data[i][140],
            # selling point 7 or product__bullets__6
            data[i][141],
            # product__configuration__codes is not available
            None,
            # The product__multipack_quantity and carton count refer to the same concept of the quantity of items in a pack or carton.
            data[i][56],
            # product country of origin alpha_3
            get_country_alpha3(data[i][129]),
            # product__parent_sku is not available
            None,
            #attrib__arm_height is not available
            None,
            # attrib__assembly_required is not available
            None,
            # attrib__back_material is not available
            None,
            # attrib__blade_finish is not available
            None,
            # bulb 1 include or attrib__bulb_included
            data[i][83],
            # bulb 1 type or can be attrib__bulb_type
            data[i][81],
            # attrib__color or cord color
            data[i][113],
            # attrib__cord_length or cord length (inches)
            convert_to_inches(data[i][114], data[0][114]),
            # attrib__design_id is not available
            None,
            # attrib__designer is not available
            None,
            # attrib__distressed_finish is not available,
            None,
            # attrib__fill is not available,
            None,
            # item finish or attrib__finish
            data[i][26],
            # attrib__frame_color is not available
            None,
            # attrib__hardwire is not available,
            None,
            # attrib__kit is not available,
            None,
            # attrib__leg_color is not available,
            None,
            # attrib__leg_finish is not available
            None,
            # item materials
            data[i][24],
            # attrib__number_bulbs can be bulb 1 count
            data[i][79],
            # attrib__orientation is not available
            None,
            # attrib__outdoor_safe, or outdoor is yes or no
            data[i][14],
            # attrib__pile_height is not available
            None,
            # attrib__seat_depth can be furniture seat dimensions (inches), if not in inches convert in inches
            convert_to_inches(get_attrib__seat_depth(
                data[i][127]), data[0][127]),
            # attrib__seat_height or furniture seat height (inches), height if not in inches convert in inches
            convert_to_inches(data[i][126], data[0][126]),
            # attrib__seat_width
            convert_to_inches(get_attrib__seat_width(
                data[i][127]), data[0][127]),
            # "attrib__shade" or shade/glass description
            data[i][104],
            # attrib__size is not available
            None,
            # switch type or attrib__bulb_type
            data[i][94],
            # attrib__ul_certified is not available,
            None,
            # attrib__warranty_years is not available
            None,
            # bulb 1 wattage
            data[i][80],
            # attrib__weave is not available
            None,
            # attrib__weight_capacity can be furniture weight capacity (pounds), weight if not in pounds convert in ponds
            convert_to_pounds(data[i][128], data[0][128]),
            # box or carton 1 or boxes__0__weight, weight if not in pounds convert in pounds
            convert_to_pounds(data[i][61], data[0][61]),
            # box or carton 1 or boxes__0__length, length if not in inches convert in inches
            convert_to_inches(data[i][59], data[0][59]),
            # box or carton 1 or boxes__0__height, height if not in inches convert in inches
            convert_to_inches(data[i][60], data[0][60]),
            # box or carton 1 or boxes__0__width, width if not in inches convert in inches
            convert_to_inches(data[i][58], data[0][58]),
            # boxes__1__weight or carton 2 weight (pounds), weight if not in pounds convert in ponds
            convert_to_pounds(data[i][66], data[0][66]),
            # boxes__1__length or carton 2 length (inches), length if not in inches convert in inches,
            convert_to_inches(data[i][64], data[0][64]),
            # boxes__1__height or carton 2 height (inches), height if not in inches convert in inches,
            convert_to_inches(data[i][65], data[0][65]),
            # boxes__1__width or carton 2 width (inches), width if not in inches convert in inches
            convert_to_inches(data[i][63], data[0][63]),
            # boxes__2__weight or carton 3 weight (pounds), weight if not in pounds convert in inches
            convert_to_pounds(data[i][71], data[0][71]),
            # boxes__2__length or carton 3 length (inches), length if not in inches convert in inches,
            convert_to_inches(data[i][69], data[0][69]),
            # boxes__2__height or carton 3 height (inches), height if not in inches convert in inches,
            convert_to_inches(data[i][70], data[0][70]),
            # boxes__2__width or carton 3 width (inches), width if not in inches convert in inches
            convert_to_inches(data[i][68], data[0][68]),
            # boxes__3__weight not available,
            None,
            # boxes__3__length not available
            None,
            # boxes__3__height Not available
            None,
            # boxes__3__width Not available
            None,
            # item style or product__styles
            data[i][51],
        ]
        new_data.append(data[i])

    # Write rows to formatted.csv with headers
    write_csv('formatted.csv', new_data, headers)
    print("formatted.csv file created successfully please check on directory")


if __name__ == '__main__':
    main()
