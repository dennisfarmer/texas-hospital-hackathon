from numpy.random import ranf
from numpy import sqrt

vendors = ["H.E.B.", "Whole Foods", "Kroger"]

city_locations = {'The Woodlands': (30.1658, -95.4613), 'Austin':(30.2672, -97.7431), 'Houston':(29.7604, -95.3698), 'Kingwood':(30.0500, -95.1845), 'Humble':(29.9988, -95.2622), 'Bellaire':(29.7058, -95.4588), 'Cypress':(29.9717, -95.6938), 'Pearland':(29.5636, -95.2860), 'Katy':(29.7858, -95.8245), 'McAllen':(26.2034, -98.2300), 'Sugar Land':(29.5984, -95.6226), 'Webster':(29.5377, -95.1183)}


# for testing purposes, generate random (lat, long)
def rand_loc(lat, long):
    return dim[0] - dim[1] for dim in zip(
        (lat, long), [n-0.5 for n in np.ranf(size=2)]

        #lat is y
def calc_distance_miles(a, b)
        # rough parameter that averages lat->mi and long->mi, more accurate estimates would use trig
        miles_per_latlong = 64
        delta_lat = a[0] - b[0]
        delta_long = a[1] - b[1]
        return sqrt(delta_lat**2 + delta_long**2) * miles_per_latlong


def get_vendors(city="all"):
    if city=="all":
        L = []
        for v in vendors:
            for c in city_locations:
                L.append((f"{v} - {c}", f"{v} - {c}"))
        return L
    else:
        if city not in [c for c in city_locations]:
            raise IndexError()
            return
        else:
            return [(f"{v} - {city}", f"{v} - {city}") for v in vendors]


# TODO: implement inventory system (that's like a bunch of work so no lol)


def create_purchase(customer:"users.User_Profile", order: "orders.Order", vendor: str):
    import sys, os
    from .models import Order, Order_Purchase
    sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))
    from users.models import User_Profile
    Order_Purchase.objects.create(customer=customer,
                                  order=order,
                                  vendor=vendor)




datapath = os.path.join(os.path.dirname(__file__), "data/")

generic_food_csv = os.path.join(datapath, "alexandra-generic-food-database/data/generic_food.csv")
custom_food_csv = os.path.join(datapath, "custom_food.csv")

def get_generic_foods() -> pd.DataFrame:
    # https://data.world/alexandra/generic-food-database
    if os.path.exists(generic_food_csv):
        try:
            generic_foods = pd.read_csv(generic_food_csv)
        except EmptyDataError as err:
            print(f"pandas.errors.EmptyDataError: {err}", "foods.py: returning empty df", sep="\n")
            return pd.DataFrame()
        generic_foods.rename(columns={"food_name": "name", "group": "food_group"}, inplace=True)
        generic_foods = generic_foods[generic_foods.columns.intersection(["name", "food_group"])]
        return generic_foods
    else:
        return pd.DataFrame()

# handle specific error catching when reading custom_food csv
# return either a custom_food dataframe or an empty dataframe
def get_custom_foods(f=custom_food_csv) -> pd.DataFrame:
    if os.path.exists(f):
        try:
            food_df = pd.read_csv(f).set_index("id")
            try:
                assert list(food_df.columns.values) == ["name", "food_group"]
            except AssertionError:
                print(f"AssertionError: {list(food_df.columns.values)} does not match [\"name\", \"food_group\"]", "foods.py: returning empty df", sep="\n")
                food_df = pd.DataFrame()
        except EmptyDataError as err:
            print(f"pandas.errors.EmptyDataError: {err}", "foods.py: returning empty df", sep="\n")
            food_df = pd.DataFrame()
    else:
        food_df = pd.DataFrame()
    return food_df

def write_foods_to_database(force=False):
    if Menu_Item.objects.all().count() > 0:
        if force:
            # DELETE FROM Menu_Item;
            Menu_Item.objects.all().delete()
        else:
            print("foods.py: Database already populated, specify --force to force rewrite")

    if Menu_Item.objects.all().count() == 0:
        foods = get_generic_foods()
        for index, row in foods.iterrows():
            item = Menu_Item.objects.create(
                name = row["name"],
                food_group = row["food_group"]
            )
            # update existing entries in through table that links together orders 
            # and their respective menu_items by using the order_item.menu_item_name entry
            Order_Item.objects.filter(menu_item_name=item.name).update(menu_item=item)
        # also update db with custom food values if they exist
        if os.path.exists(custom_food_csv):
            foods = get_custom_foods()
            for index, row in foods.iterrows():
                item = Menu_Item.objects.create(
                    pk = index,
                    name = row["name"],
                    food_group = row["food_group"]
                )
                # update existing entries in through table that links together orders 
                # and their respective menu_items by using the order_item.menu_item_name entry
                #
                # Note: may cause unnecessary overwrite of items if custom_foods and generic_foods happen
                # to have entries with the same name, but there will be no errors since they don't
                # share the same primary key
                Order_Item.objects.filter(menu_item_name=item.name).update(menu_item=item)

# Return list of unique food_groups
def get_food_groups():
    try:
        L= Menu_Item.objects.order_by("food_group").values_list("food_group", flat=True).distinct()
    except OperationalError as err:
        print("django.db.utils.OperationalError: ", err, sep="")
        print("foods.py: Non-fatal error, continuing...")
        L = ["Unclassified"]
    return L

# Used by orders.order_forms.ItemCreationForm to backup new menu_items to csv
# so that they can be recalled after refreshing (removing all entries from)
# the database
def backup_custom_food(pk, name, food_group):
    food_df = get_custom_foods()
    custom_food = pd.Series({"name": name,"food_group": food_group}, name=pk)
    food_df = food_df.append(custom_food)
    food_df.to_csv(custom_food_csv, index_label="id")


def remove_custom_foods():
    if os.path.exists(custom_food_csv):
        food_df = get_custom_foods()
        for index, row in food_df.iterrows():
            item = Menu_Item.objects.filter(pk=index).first()
            if item is not None:
                try:
                    item.delete()
                    print("foods.py: deleting ", item, " at pk=", index, sep="")
                except:
                    pass
        os.delete(custom_food_csv)
    else:
        print("foods.py: nothing to delete")


if __name__ == "__main__":
    pass
