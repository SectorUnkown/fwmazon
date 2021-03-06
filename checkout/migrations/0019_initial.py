# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'ShippingDestination'
        db.create_table(u'checkout_shippingdestination', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('short_name', self.gf('django.db.models.fields.CharField')(max_length=64)),
            ('system', self.gf('django.db.models.fields.CharField')(max_length=64)),
            ('shipping_cost', self.gf('django.db.models.fields.DecimalField')(default=0.0, max_digits=15, decimal_places=2, blank=True)),
            ('active', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('delay', self.gf('django.db.models.fields.IntegerField')()),
        ))
        db.send_create_signal(u'checkout', ['ShippingDestination'])

        # Adding model 'Order'
        db.create_table(u'checkout_order', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('buyer', self.gf('django.db.models.fields.related.ForeignKey')(related_name='orders', to=orm['account.User'])),
            ('contractor', self.gf('django.db.models.fields.related.ForeignKey')(related_name='orders_contracted', null=True, to=orm['account.User'])),
            ('payment', self.gf('django.db.models.fields.related.ForeignKey')(related_name='order', to=orm['checkout.Payment'])),
            ('total_price', self.gf('django.db.models.fields.DecimalField')(default='0', max_digits=15, decimal_places=2, blank=True)),
            ('elements_price', self.gf('django.db.models.fields.DecimalField')(default='0', max_digits=15, decimal_places=2, blank=True)),
            ('volume', self.gf('django.db.models.fields.FloatField')(default=0.0)),
            ('shipping_fee', self.gf('django.db.models.fields.DecimalField')(default='0', max_digits=15, decimal_places=2, blank=True)),
            ('shipping_destination', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['checkout.ShippingDestination'])),
            ('to_be_fitted', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('priority_flag', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('order_status', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('contracted_at', self.gf('django.db.models.fields.DateTimeField')(null=True)),
            ('created_at', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('updated_at', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
        ))
        db.send_create_signal(u'checkout', ['Order'])

        # Adding model 'OrderElement'
        db.create_table(u'checkout_orderelement', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('order', self.gf('django.db.models.fields.related.ForeignKey')(related_name='elements', to=orm['checkout.Order'])),
            ('element_type', self.gf('django.db.models.fields.CharField')(max_length=20)),
            ('doctrine_fit', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['shop.DoctrineFit'], null=True, blank=True)),
            ('item', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['eve.InvType'], null=True, blank=True)),
            ('price', self.gf('django.db.models.fields.DecimalField')(default=0.0, max_digits=15, decimal_places=2, blank=True)),
            ('amount', self.gf('django.db.models.fields.IntegerField')(max_length=5)),
        ))
        db.send_create_signal(u'checkout', ['OrderElement'])

        # Adding model 'Payment'
        db.create_table(u'checkout_payment', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('status', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('key', self.gf('django.db.models.fields.CharField')(max_length=35)),
            ('transaction', self.gf('django.db.models.fields.related.ForeignKey')(related_name='payment', null=True, to=orm['eve.CorpWalletJournalEntry'])),
            ('created_at', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('updated_at', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
        ))
        db.send_create_signal(u'checkout', ['Payment'])


    def backwards(self, orm):
        # Deleting model 'ShippingDestination'
        db.delete_table(u'checkout_shippingdestination')

        # Deleting model 'Order'
        db.delete_table(u'checkout_order')

        # Deleting model 'OrderElement'
        db.delete_table(u'checkout_orderelement')

        # Deleting model 'Payment'
        db.delete_table(u'checkout_payment')


    models = {
        u'account.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Group']", 'symmetrical': 'False', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_contractor': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_manager': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        u'auth.group': {
            'Meta': {'object_name': 'Group'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        u'auth.permission': {
            'Meta': {'ordering': "(u'content_type__app_label', u'content_type__model', u'codename')", 'unique_together': "((u'content_type', u'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['contenttypes.ContentType']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        u'checkout.order': {
            'Meta': {'object_name': 'Order'},
            'buyer': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'orders'", 'to': u"orm['account.User']"}),
            'contracted_at': ('django.db.models.fields.DateTimeField', [], {'null': 'True'}),
            'contractor': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'orders_contracted'", 'null': 'True', 'to': u"orm['account.User']"}),
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'elements_price': ('django.db.models.fields.DecimalField', [], {'default': "'0'", 'max_digits': '15', 'decimal_places': '2', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'order_status': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'payment': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'order'", 'to': u"orm['checkout.Payment']"}),
            'priority_flag': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'shipping_destination': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['checkout.ShippingDestination']"}),
            'shipping_fee': ('django.db.models.fields.DecimalField', [], {'default': "'0'", 'max_digits': '15', 'decimal_places': '2', 'blank': 'True'}),
            'to_be_fitted': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'total_price': ('django.db.models.fields.DecimalField', [], {'default': "'0'", 'max_digits': '15', 'decimal_places': '2', 'blank': 'True'}),
            'updated_at': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'volume': ('django.db.models.fields.FloatField', [], {'default': '0.0'})
        },
        u'checkout.orderelement': {
            'Meta': {'object_name': 'OrderElement'},
            'amount': ('django.db.models.fields.IntegerField', [], {'max_length': '5'}),
            'doctrine_fit': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['shop.DoctrineFit']", 'null': 'True', 'blank': 'True'}),
            'element_type': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'item': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['eve.InvType']", 'null': 'True', 'blank': 'True'}),
            'order': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'elements'", 'to': u"orm['checkout.Order']"}),
            'price': ('django.db.models.fields.DecimalField', [], {'default': '0.0', 'max_digits': '15', 'decimal_places': '2', 'blank': 'True'})
        },
        u'checkout.payment': {
            'Meta': {'object_name': 'Payment'},
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'key': ('django.db.models.fields.CharField', [], {'max_length': '35'}),
            'status': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'transaction': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'payment'", 'null': 'True', 'to': u"orm['eve.CorpWalletJournalEntry']"}),
            'updated_at': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'})
        },
        u'checkout.shippingdestination': {
            'Meta': {'object_name': 'ShippingDestination'},
            'active': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'delay': ('django.db.models.fields.IntegerField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'shipping_cost': ('django.db.models.fields.DecimalField', [], {'default': '0.0', 'max_digits': '15', 'decimal_places': '2', 'blank': 'True'}),
            'short_name': ('django.db.models.fields.CharField', [], {'max_length': '64'}),
            'system': ('django.db.models.fields.CharField', [], {'max_length': '64'})
        },
        u'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'eve.apikey': {
            'Meta': {'object_name': 'APIKey'},
            'id': ('django.db.models.fields.IntegerField', [], {'primary_key': 'True'}),
            'user': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['account.User']", 'unique': 'True', 'null': 'True'}),
            'vcode': ('django.db.models.fields.CharField', [], {'max_length': '64'})
        },
        u'eve.corpwallet': {
            'Meta': {'object_name': 'CorpWallet'},
            'account_key': ('django.db.models.fields.IntegerField', [], {'default': '1000'}),
            'apikey': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['eve.APIKey']"}),
            'balance': ('django.db.models.fields.DecimalField', [], {'default': "'0'", 'max_digits': '30', 'decimal_places': '2'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'wallet_id': ('django.db.models.fields.IntegerField', [], {'primary_key': 'True'})
        },
        u'eve.corpwalletjournalentry': {
            'Meta': {'object_name': 'CorpWalletJournalEntry'},
            'amount': ('django.db.models.fields.DecimalField', [], {'default': "'0'", 'max_digits': '30', 'decimal_places': '2'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'reason': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'ref_id': ('django.db.models.fields.BigIntegerField', [], {}),
            'ref_type_id': ('django.db.models.fields.IntegerField', [], {}),
            'sender_name': ('django.db.models.fields.CharField', [], {'max_length': '65'}),
            'transaction_date': ('django.db.models.fields.DateTimeField', [], {}),
            'wallet': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'entries'", 'to': u"orm['eve.CorpWallet']"})
        },
        u'eve.invcategory': {
            'Meta': {'ordering': "['id']", 'object_name': 'InvCategory'},
            'description': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'icon_id': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.IntegerField', [], {'unique': 'True', 'primary_key': 'True'}),
            'is_published': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        u'eve.invgroup': {
            'Meta': {'ordering': "['id']", 'object_name': 'InvGroup'},
            'allow_anchoring': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'allow_manufacture': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'allow_recycle': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'category': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['eve.InvCategory']", 'null': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {}),
            'icon_id': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.IntegerField', [], {'unique': 'True', 'primary_key': 'True'}),
            'is_anchored': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_fittable_non_singleton': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_published': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '150'}),
            'use_base_price': ('django.db.models.fields.BooleanField', [], {'default': 'False'})
        },
        u'eve.invmarketgroup': {
            'Meta': {'ordering': "['id']", 'object_name': 'InvMarketGroup'},
            'description': ('django.db.models.fields.TextField', [], {'max_length': '300012', 'null': 'True', 'blank': 'True'}),
            'has_items': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'icon_id': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.IntegerField', [], {'unique': 'True', 'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'parent': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['eve.InvMarketGroup']", 'null': 'True', 'blank': 'True'})
        },
        u'eve.invtype': {
            'Meta': {'ordering': "['id']", 'object_name': 'InvType'},
            'base_price': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'capacity': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'chance_of_duplicating': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'group': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['eve.InvGroup']", 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.IntegerField', [], {'unique': 'True', 'primary_key': 'True'}),
            'is_published': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'market_group': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['eve.InvMarketGroup']", 'null': 'True', 'blank': 'True'}),
            'mass': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'}),
            'portion_size': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'volume': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'})
        },
        u'shop.doctrinefit': {
            'Meta': {'object_name': 'DoctrineFit'},
            'bought': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'creator': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['account.User']"}),
            'description': ('django.db.models.fields.TextField', [], {}),
            'fit': ('django.db.models.fields.TextField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'price': ('django.db.models.fields.DecimalField', [], {'default': "'0'", 'max_digits': '15', 'decimal_places': '2', 'blank': 'True'}),
            'ship': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['eve.InvType']"}),
            'status': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'updated_at': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'volume': ('django.db.models.fields.FloatField', [], {'default': '0.0'})
        }
    }

    complete_apps = ['checkout']