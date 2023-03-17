from cdf.utils import GetClient

client = GetClient()
token = client.iam.token.inspect()
print(token.capabilities)
