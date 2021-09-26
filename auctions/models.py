from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models.base import Model
from django.db.models.deletion import CASCADE, RESTRICT
from django.utils import tree

class User(AbstractUser):
    pass
    def __str__(self):
        return f" {self.username}: {self.email}:"


class Listing(models.Model):


    APPLIANCES ='Appliances'
    APPS_GAMES='Apps & Games'
    ARTS_CRAFTS_SEWING='Arts, Crafts, & Sewing'
    AUTOMOTIVE_PARTS_ACCESSORIES='Automotive Parts & Accessories'
    BABY='Baby'
    BEAUTY_PERSONAL_CARE='Beauty & Personal Care'
    BOOKS='Books'
    CDS_VINYL='CDs & Vinyl'
    CELL_PHONES_ACCESSORIES='Cell Phones & Accessories'
    CLOTHING_SHOES_AND_JEWELRY='Clothing, Shoes and Jewelry'
    COLLECTIBLES_FINE_ART='Collectibles & Fine Art'
    COMPUTERS='Computers'
    ELECTRONICS='Electronics'
    GARDEN_OUTDOOR='Garden & Outdoor'
    GROCERY_GOURMET_FOOD='Grocery & Gourmet Food'
    HANDMADE='Handmade'
    HEALTH_HOUSEHOLD_BABY_CARE='Health, Household & Baby Care'
    HOME_KITCHEN='Home & Kitchen'
    INDUSTRIAL_SCIENTIFIC='Industrial & Scientific'
    KINDLE='Kindle'
    LUGGAGE_TRAVEL_GEAR='Luggage & Travel Gear'
    MOVIES_TV='Movies & TV'
    MUSICAL_INSTRUMENTS='Musical Instruments'
    OFFICE_PRODUCTS='Office Products'
    PET_SUPPLIES='Pet Supplies'
    SPORTS_OUTDOORS='Sports & Outdoors'
    TOOLS_HOME_IMPROVEMENT='Tools & Home Improvement'
    TOYS_GAMES='Toys & Games'
    VIDEO_GAMES='Video Games'









    LISTING_CATAGORIES = [
        (APPLIANCES,"Appliances"),
        (APPS_GAMES,"Apps & Games"),
        (ARTS_CRAFTS_SEWING,"Arts, Crafts, & Sewing"),
        (AUTOMOTIVE_PARTS_ACCESSORIES,"Automotive Parts & Accessories"),
        (BABY,"Baby"),
        (BEAUTY_PERSONAL_CARE,"Beauty & Personal Care"),
        (BOOKS,"Books"),
        (CDS_VINYL,"CDs & Vinyl"),
        (CELL_PHONES_ACCESSORIES,"Cell Phones & Accessories"),
        (CLOTHING_SHOES_AND_JEWELRY,"Clothing, Shoes and Jewelry"),
        (COLLECTIBLES_FINE_ART,"Collectibles & Fine Art"),
        (COMPUTERS,"Computers"),
        (ELECTRONICS,"Electronics"),
        (GARDEN_OUTDOOR,"Garden & Outdoor"),
        (GROCERY_GOURMET_FOOD,"Grocery & Gourmet Food"),
        (HANDMADE,"Handmade"),
        (HEALTH_HOUSEHOLD_BABY_CARE,"Health, Household & Baby Care"),
        (HOME_KITCHEN,"Home & Kitchen"),
        (INDUSTRIAL_SCIENTIFIC,"Industrial & Scientific"),
        (KINDLE,"Kindle"),
        (LUGGAGE_TRAVEL_GEAR,"Luggage & Travel Gear"),
        (MOVIES_TV,"Movies & TV"),
        (MUSICAL_INSTRUMENTS,"Musical Instruments"),
        (OFFICE_PRODUCTS,"Office Products"),
        (PET_SUPPLIES,"Pet Supplies"),
        (SPORTS_OUTDOORS,"Sports & Outdoors"),
        (TOOLS_HOME_IMPROVEMENT,"Tools & Home Improvement"),
        (TOYS_GAMES,"Toys & Games"),
        (VIDEO_GAMES,"Video Games")

    ]




    OPEN = 'AT'
    CLOSE = 'CL'
    LISTING_STATUS = [
        (OPEN, 'Open'),
        (CLOSE, 'Close')
    ]


    user = models.ForeignKey(
        User, on_delete=models.CASCADE, null=True, related_name="item_owner")

    title = models.CharField(max_length=50,default='Title')
    description = models.CharField(max_length=150, default='Description')
    url = models.URLField(max_length=1000, null=True)
  
    price = models.FloatField(default=0.00)

    status = models.CharField(
        max_length=2,
        choices=LISTING_STATUS,
        default=OPEN,
    )


    catagory = models.CharField(max_length=40,choices = LISTING_CATAGORIES)


    def __str__(self):
        return f"Item {self.title}:  {self.description}: {self.url}: {self.user}: {self.price}"

class Bid(models.Model):

    WON = 'WN'
    LOST = 'LS'
    PENDING = "PD"

    BID_STATUS = [
        (WON, 'WON'),
        (LOST, 'LOST'),
        (PENDING,"PENDING")
    ]

    bid_value = models.FloatField(default=0)
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, null=True, related_name="bidder")
    listing = models.ForeignKey(Listing,on_delete=CASCADE,null = True, related_name="biddings")
    win_status  =  models.CharField(
        max_length=2,
        choices=BID_STATUS,
        default=PENDING
    )

    def __str__(self):
        return f" {self.bid_value}: by {self.user}: item {self.listing}"


class Comment(models.Model):
    comment = models.CharField(max_length=256,default='comment')
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, null=True, related_name="comment")
    listing = models.ForeignKey(Listing,on_delete=CASCADE,null = True, related_name="listings")

    def __str__(self):
        return f"User {self.user}: commented {self.comment}: on {self.listing}"



class Watchlist(models.Model):

    user = models.ForeignKey(
        User, on_delete=models.RESTRICT, null=False, related_name="potential_buyer")
    listing = models.ForeignKey(Listing,on_delete=RESTRICT,null = False, related_name="wishlist")

    def __str__(self):
        return f"  {self.user}: wishlist {self.listing}"







