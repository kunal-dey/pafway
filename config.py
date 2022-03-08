# mail part
REGISTERED_MAIL = 'kunal.dey@ivanwebsolutions.com'
MAIL_API_KEY = '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'

# app part
SECRET = 'Kunal Dey'

# database part (MONGO DB)
USERNAME = 'kunal'
PASSWORD = 'kunal22061994'
HOSTNAME = 'e-commerce-app-shard-00-00.ysjtb.mongodb.net:27017,e-commerce-app-shard-00-01.ysjtb.mongodb.net:27017,e-commerce-app-shard-00-02.ysjtb.mongodb.net:27017'
DATABASE = 'mypafway'
DATABASE_URI = "mongodb://{0}:{1}@{2}/{3}?ssl=true&replicaSet=atlas-r3qvd9-shard-0&authSource=admin&retryWrites=true&w=majority".format(
        USERNAME, PASSWORD, HOSTNAME, DATABASE
)


