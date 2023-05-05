from django.db import models


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


class copier_accounts(models.Model):
    id = models.AutoField(primary_key=True)
    UserID = models.IntegerField()
    AccountNumber = models.CharField(max_length=50)
    BrokerName = models.CharField(max_length=50)
    Token = models.CharField(max_length=255)
    Status = models.CharField(max_length=10)

    def __str__(self):
        return f"{self.AccountNumber} ({self.BrokerName})"


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


class copier_logs(models.Model):
    id = models.AutoField(primary_key=True)
    AccountID = models.IntegerField()
    OrderID = models.IntegerField()
    LogTime = models.DateTimeField(auto_now_add=True)
    Message = models.TextField()

    def __str__(self):
        return f"{self.LogTime} - Order {self.OrderID} - {self.Message}"