import json
import datetime
from decimal import Decimal
from celery import task
from django.utils import timezone
import eveapi
from fwmazon.redisevecache import RedisEveAPICacheHandler
from evejournal import EveJournal
from checkout.models import Payment, MONEY_RECEIVED
from eve.models import APIKey, CorpWallet, CorpWalletJournalEntry, InvType, ItemPrice
from shop.models import DoctrineFit
from celery.utils.log import get_task_logger
l = get_task_logger('fwmazon')


# TODO: Add ammo support, and we can do better
@task()
def update_fit(fit_id):
    l.info('Starting update_fit task DoctrineFit#%s' % fit_id, extra={'fit_id': fit_id})
    try:
        doctrine_fit = DoctrineFit.objects.get(pk=fit_id)
    except DoctrineFit.DoesNotExist:
        return False
    if doctrine_fit.updated_at > timezone.now() or doctrine_fit.status == 0:
        return False
    fit = json.loads(doctrine_fit.fit)
    price = Decimal(0.0)
    try:
        p = ItemPrice.objects.get(item_id=fit['ship']['ship_id'])
    except ItemPrice.DoesNotExist:
        p = ItemPrice()
        p.item = InvType.objects.get(pk=fit['ship']['ship_id'])
        p.save()
    p.update_price(force=True)
    price += p.price
    for m in fit['modules']:
        try:
            p = ItemPrice.objects.get(item_id=m['id'])
        except ItemPrice.DoesNotExist:
            p = ItemPrice()
            p.item = InvType.objects.get(pk=m['id'])
            p.save()
        p.update_price(force=True)
        price += p.price
    for d in fit['drones']:
        try:
            p = ItemPrice.objects.get(item_id=d['id'])
        except ItemPrice.DoesNotExist:
            p = ItemPrice()
            p.item = InvType.objects.get(pk=m['id'])
            p.save()
        p.update_price(force=True)
        price += (p.price * d['amount'])
    doctrine_fit.status = 1
    doctrine_fit.price = price
    doctrine_fit.save()
    l.info('Ended update_fit task DoctrineFit#%s' % fit_id, extra={'fit_id': fit_id})


# TODO: Make it so that it updates more than one price
@task()
def update_price_item(item_ids=[]):
    l.info('Starting update_price_item', extra={'items': item_ids})
    for item_id in item_ids:
        item = ItemPrice.objects.get(pk=item_id)
        item.update_price(force=True)
        return item.price


@task()
def process_journal():
    l.info('Starting process_journal')
    wallets = CorpWallet.objects.all()
    for wallet in wallets:
        journal = EveJournal(wallet.account_key)
        for page in journal:
            if page is None:
                break
            for transaction in page:
                try:
                    entry = CorpWalletJournalEntry.objects.get(ref_id=transaction.refID)
                except CorpWalletJournalEntry.DoesNotExist:
                    date = timezone.make_aware(datetime.datetime.utcfromtimestamp(transaction.date), timezone.utc)
                    entry_data = {
                        'wallet': wallet,
                        'transaction_date': date,
                        'ref_type_id': transaction.refTypeID,
                        'ref_id': transaction.refID,
                        'sender_name': transaction.ownerName1,
                        'amount': Decimal(transaction.amount),
                        'reason': transaction.reason,
                    }
                    entry = CorpWalletJournalEntry(**entry_data)
                    entry.save()
                    if entry.ref_type_id == 10:
                        process_transaction.delay(entry.id, delay=5)


@task()
def process_transaction(transaction_id):
    l.info('Starting process_transaction', extra={'transaction': transaction_id})
    try:
        transaction = CorpWalletJournalEntry.objects.get(ref_id=transaction_id)
    except CorpWalletJournalEntry.DoesNotExist:
        raise CorpWalletJournalEntry.DoesNotExist
    reason = transaction.reason.replace(' ', '').rstrip('\n')[5:]
    try:
        payment = Payment.objects.get(key=reason)
    except Payment.DoesNotExist:
        return
    if payment.status == MONEY_RECEIVED or transaction.amount != payment.order.total_price:
        return
    payment.status = MONEY_RECEIVED
    payment.transaction = transaction
    payment.save()


@task()
def update_wallets():
    l.info('Starting update_wallets')
    api_key = APIKey.objects.get(pk=2338850)
    api = eveapi.EVEAPIConnection(cacheHandler=RedisEveAPICacheHandler(debug=True)).auth(keyID=api_key.id, vCode=api_key.vcode)
    balance = api.corp.AccountBalance()
    for account in balance.accounts:
        try:
            wallet = CorpWallet.objects.get(wallet_id=account.accountID)
        except CorpWallet.DoesNotExist:
            wallet_data = {'wallet_id': account.accountID, 'account_key': account.accountKey, 'apikey': api_key, 'name': 'Not named #%s' % account.accountID}
            wallet = CorpWallet(**wallet_data)
        wallet.balance = Decimal(account.balance)
        wallet.save()
