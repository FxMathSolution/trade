from django.db import models
import hashlib

class copier_users(models.Model):
    UserID = models.AutoField(primary_key=True)
    FirstName = models.CharField(max_length=50)
    LastName = models.CharField(max_length=50)
    Email = models.EmailField(unique=True)
    Password = models.CharField(max_length=255)
    Phone = models.CharField(max_length=20)
    Status = models.CharField(max_length=10)

    def __str__(self):
        return f"{self.FirstName} {self.LastName}"

    @staticmethod
    def authenticate(email, password):
        try:
            user = copier_users.objects.get(Email=email, Password=hashlib.md5(password.encode()).hexdigest())
            return user.UserID
        except copier_users.DoesNotExist:
            return -30

class copier_accounts(models.Model):
    id = models.AutoField(primary_key=True)
    UserID = models.IntegerField()
    AccountNumber = models.CharField(max_length=50)
    BrokerName = models.CharField(max_length=50)
    Token = models.CharField(max_length=255)
    Status = models.CharField(max_length=10)

    def __str__(self):
        return f"{self.AccountNumber} ({self.BrokerName})"

    @staticmethod
    def get_orders(account_id):
        return copier_orders.objects.filter(AccountID=account_id)

class copier_orders(models.Model):
    id = models.AutoField(primary_key=True)
    AccountID = models.IntegerField()
    OrderID = models.IntegerField()
    Symbol = models.CharField(max_length=50)
    Type = models.CharField(max_length=10)
    Volume = models.FloatField()
    OpenTime = models.DateTimeField()
    OpenPrice = models.FloatField()
    SL = models.FloatField()
    TP = models.FloatField()
    CloseTime = models.DateTimeField(null=True)
    ClosePrice = models.FloatField(null=True)
    Commission = models.FloatField()
    Swap = models.FloatField()
    Profit = models.FloatField()
    Status = models.CharField(max_length=10)

    def __str__(self):
        return f"{self.OrderID} ({self.Symbol})"

    @staticmethod
    def filter_orders(symbol=None, order_type=None, status=None):
        orders = copier_orders.objects.all()
        if symbol:
            orders = orders.filter(Symbol=symbol)
        if order_type:
            orders = orders.filter(Type=order_type)
        if status:
            orders = orders.filter(Status=status)
        return orders

    @staticmethod
    def compute_total_profit():
        return copier_orders.objects.aggregate(total_profit=models.Sum('Profit'))['total_profit'] or 0.0

class copier_logs(models.Model):
    id = models.AutoField(primary_key=True)
    AccountID = models.IntegerField()
    OrderID = models.IntegerField()
    LogTime = models.DateTimeField(auto_now_add=True)
    Message = models.TextField()

    def __str__(self):
        return f"{self.LogTime} - Order {self.OrderID} - {self.Message}"
