from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import logging
from ibm_watson_interface.views import ask_watson
import os
import signal
import sys
from hackerearth.models import Conversation_bot_context
from hackerearth.models import Failure
from hackerearth.models import Client
from hackerearth.models import Product
from math import ceil
from django.db.models import Avg

client_list = ('MOSCONI INC','FAGOTO','HOUSING CO','RUNTE INC','KUPHAL-GREEN')
product_list = ('ALUMINUM STEEL', 'ALUMINUM PIPE', 'BRASS ROUND BAR', 'BRASS SQUARE BAR', 'COPPER ROUND BAR', 'COPPER SQUARE BAR', 'STEEL BEAM', 'STEEL PIPE', 'STEEL PLATE')
conveyor_belt_list = ('BELT A','BELT B','BELT C','BELT D')
machine_list = ('CLAMPING STRAPS', 'COUNTER-BEARINGS', 'MOTOR BRACKET', 'PULLEY')
failure_mode_list = ('ARM DERAILED','BY-PRODUCTS DELAY','CLEANING/INSPECTION','CRF ELECTRICAL ISSUES','EMPTY','EXHAUSTER FAILURE','GALLERY ISSUES','HIGH TEMPS','INSULATORS ADRIFT','LOW','SENSOR FAILURE','SHEARED','TEE BAR DISTORTED','UNKNOWN ELECTRICAL FAILURE','UNKNOWN MECHANICAL FAILURE','UNPLANNED CHANGE DUE TO FAILURE')
#from django.db import connection
#References:
#https://github.com/python-telegram-bot/python-telegram-bot/wiki/Introduction-to-the-API
#https://github.com/python-telegram-bot/python-telegram-bot/wiki/Extensions-%E2%80%93-Your-first-Bot

def start(update, context):
    effective_user = update['_effective_user']
    id_user = effective_user['id']
    user_name = effective_user['first_name']
    response = "Hello {}! My name is PAM and I am glad to help. How can I assist you?".format(user_name)
    context.bot.send_message(chat_id=update.effective_chat.id, text=response)
    Conversation_bot_context.objects.filter(conversation=id_user).delete()

def non_command(update, context):
    #Echo:
    #context.bot.send_message(chat_id=update.effective_chat.id, text=update.message.text)

    watson_response = ask_watson(update.message.text)
    print(update.message.text)
    print(watson_response)
    if len(watson_response.get('intents')) == 0:
        intent = 'No intent'
    else:
        intent = watson_response.get('intents')[0].get('intent')
    if len(watson_response.get('entities')) == 0:
        entity = 'No entity'
    else:
        entity = dict( [(v.get('entity'),v.get("value")) for v in watson_response.get('entities')])
    ##print(intent)
    define_action(update,context,intent,entity)
    #response = "Bubu knows best"
    #context.bot.send_message(chat_id=update.effective_chat.id, text=response)

def define_action(update,context,intents,entities):
    effective_user = update['_effective_user']
    id_user = effective_user['id']
    user_name = effective_user['first_name']

    intent_hist = ''

    intent_hist_query = Conversation_bot_context.objects.filter(conversation=id_user,value_type='intent').values('value')
    print('intent_hist_query',len(intent_hist_query))
    if intents == 'No intent' and len(intent_hist_query) > 0:
        intents = intent_hist_query[0]['value']
        intent_hist = intent_hist_query[0]['value']
    print("intent",intents)
    if intents == 'insert_order':
        if intent_hist == '':
            conversation_context = Conversation_bot_context(conversation=id_user,value_type='intent',value='insert_order')
            conversation_context.save()
        insert_order(update,context,entities)
    if intents == 'insert_problem':
        if intent_hist == '':
            conversation_context = Conversation_bot_context(conversation=id_user,value_type='intent',value='insert_problem')
            conversation_context.save()
        insert_problem(update,context,entities)
    if intents == 'view_problem':
        if intent_hist == '':
            conversation_context = Conversation_bot_context(conversation=id_user,value_type='intent',value='view_problem')
            conversation_context.save()
        view_problem(update,context)
    if intents == 'help_pam':
        pam_help(update,context)

def insert_order(update,context,entities):

    effective_user = update['_effective_user']
    id_user = effective_user['id']
    user_name = effective_user['first_name']
    save_point_insert_order = 0


    response = ''
    product = ''
    client = ''
    deadline = ''
    quantity = ''
    client_hist = ''
    product_hist = ''


    intent_hist_query = Conversation_bot_context.objects.filter(conversation=id_user,value_type='intent').values('value')



    if len(intent_hist_query) > 0:
        intent_hist = intent_hist_query[0]['value']
    else:
        response = "OK, let's make a new order."
        context.bot.send_message(chat_id=update.effective_chat.id, text=response)

    #print(entities,'entities')

    try:
        entities['client']
    except:
        print('no client')
    else:
        if entities['client'].upper() in client_list:
            client = entities['client']
            #print('client',client)
            conversation_context = Conversation_bot_context(conversation=id_user,value_type='client',value=client)
            conversation_context.save()

    try:
        entities['product']
    except:
        print('no product')
    else:
        print('product_1',product)
        if entities['product'].upper() in product_list:
            product = entities['product']
            print('product_2',product)
            conversation_context = Conversation_bot_context(conversation=id_user,value_type='product',value=product)
            conversation_context.save()

    client_hist_query = Conversation_bot_context.objects.filter(conversation=id_user,value_type='client').values('value')
    if len(client_hist_query) > 0:
        client = client_hist_query[0]['value']

    product_hist_query = Conversation_bot_context.objects.filter(conversation=id_user,value_type='product').values('value')
    ##print('product_hist_query',product_hist_query)
    if len(product_hist_query) > 0:
        product = product_hist_query[0]['value']
    ###print('product_hist',product)

    save_point_insert_order_query = Conversation_bot_context.objects.filter(conversation=id_user,value_type='save_point_insert_order').values('value')
    if len(save_point_insert_order_query) > 0:
        save_point_insert_order = save_point_insert_order_query[0]['value']

    ###print('save_point_insert_order before',save_point_insert_order)
    print("client",client)
    print("product",product)
    print("save_point_insert_order",save_point_insert_order)
    if client == '' and save_point_insert_order < 1:

        response = 'Who is the customer?'
        context.bot.send_message(chat_id=update.effective_chat.id, text=response)
    else:
        if int(save_point_insert_order) < 1:

            #response = 'I see that the order is to {}.'.format(client)
            #context.bot.send_message(chat_id=update.effective_chat.id, text=response)

            if product == '':
                response = 'And which product {} wants? '.format(client)
                context.bot.send_message(chat_id=update.effective_chat.id,text=response)
                conversation_context = Conversation_bot_context(conversation=id_user,value_type='save_point_insert_order',value='1')
                conversation_context.save()
                save_point_insert_order_query = Conversation_bot_context.objects.filter(conversation=id_user,value_type='save_point_insert_order').values('value')

            else:
                response = 'OK, producing {} to {}'.format(product,client)
                context.bot.send_message(chat_id=update.effective_chat.id, text=response)
        else:
            if product == '':
                response = "{}, I don't have this product. Here is a list of our products:".format(user_name)
                context.bot.send_message(chat_id=update.effective_chat.id,text=response)
                response = 'ALUMINUM STEEL'
                context.bot.send_message(chat_id=update.effective_chat.id,text=response)
                response = 'ALUMINUM PIPE'
                context.bot.send_message(chat_id=update.effective_chat.id,text=response)
                response = 'BRASS ROUND BAR'
                context.bot.send_message(chat_id=update.effective_chat.id,text=response)
                response = 'BRASS SQUARE BAR'
                context.bot.send_message(chat_id=update.effective_chat.id,text=response)
                response = 'COPPER ROUND BAR'
                context.bot.send_message(chat_id=update.effective_chat.id,text=response)
                response = 'COPPER SQUARE BAR'
                context.bot.send_message(chat_id=update.effective_chat.id,text=response)
                response = 'STEEL BEAM'
                context.bot.send_message(chat_id=update.effective_chat.id,text=response)
                response = 'STEEL PIPE'
                context.bot.send_message(chat_id=update.effective_chat.id,text=response)
                response = 'STEEL PLATE'
                context.bot.send_message(chat_id=update.effective_chat.id,text=response)
            else:
                response = "OK, let's make {}.".format(product)
                context.bot.send_message(chat_id=update.effective_chat.id, text=response)
                Conversation_bot_context.objects.filter(conversation=id_user).delete()

def insert_problem(update,context,entities):
    effective_user = update['_effective_user']
    id_user = effective_user['id']
    user_name = effective_user['first_name']

    save_point_insert_problem = 0

    conveyor_belt = ''
    machine = ''
    unit = ''
    group = ''
    component = ''
    failure_mode = ''
    discipline = ''

    intent_hist_query = Conversation_bot_context.objects.filter(conversation=id_user,value_type='intent',value='insert_problem').values('value')

    if len(intent_hist_query) > 0:
        intent_hist = intent_hist_query[0]['value']
    else:
        response = 'Oh no {}, this is really sad, let me try to help!'.format(user_name)
        context.bot.send_message(chat_id=update.effective_chat.id, text=response)

    ##print(entities,'entities')

    try:
        entities['conveyor_belt']
    except:
        conveyor_belt_query = Conversation_bot_context.objects.filter(conversation=id_user,value_type='conveyor_belt').values('value')
        if len(conveyor_belt_query) > 0:
            conveyor_belt = conveyor_belt_query[0]['value']
    else:
        conveyor_belt = entities['conveyor_belt']
        ##print('conveyor_belt',conveyor_belt)
        conversation_context = Conversation_bot_context(conversation=id_user,value_type='conveyor_belt',value=conveyor_belt)
        conversation_context.save()

    try:
        entities['machine']
    except:
        machine_query = Conversation_bot_context.objects.filter(conversation=id_user,value_type='machine').values('value')
        if len(machine_query) > 0:
            machine = machine_query[0]['value']
    else:
        machine = entities['machine']
        #print('machine',machine)
        conversation_context = Conversation_bot_context(conversation=id_user,value_type='machine',value=machine)
        conversation_context.save()

    try:
        entities['unit']
    except:
        unit_query = Conversation_bot_context.objects.filter(conversation=id_user,value_type='unit').values('value')
        if len(unit_query) > 0:
            unit = unit_query[0]['value']
    else:
        unit = entities['unit']
        #print('unit',unit)
        conversation_context = Conversation_bot_context(conversation=id_user,value_type='unit',value=unit)
        conversation_context.save()

    try:
        entities['group']
    except:
        group_query = Conversation_bot_context.objects.filter(conversation=id_user,value_type='group').values('value')
        if len(group_query) > 0:
            group = group_query[0]['value']
    else:
        group = entities['group']
        #print('group',group)
        conversation_context = Conversation_bot_context(conversation=id_user,value_type='group',value=group)
        conversation_context.save()

    try:
        entities['component']
    except:
        component_query = Conversation_bot_context.objects.filter(conversation=id_user,value_type='component').values('value')
        if len(component_query) > 0:
            component = component_query[0]['value']
    else:
        component = entities['component']
        #print('component',component)
        conversation_context = Conversation_bot_context(conversation=id_user,value_type='component',value=component)
        conversation_context.save()

    try:
        entities['failure_mode']
    except:
        failure_mode_query = Conversation_bot_context.objects.filter(conversation=id_user,value_type='failure_mode').values('value')
        if len(failure_mode_query) > 0:
            failure_mode = failure_mode_query[0]['value']
    else:
        failure_mode = entities['failure_mode']
        #print('failure_mode',failure_mode)
        conversation_context = Conversation_bot_context(conversation=id_user,value_type='failure_mode',value=failure_mode)
        conversation_context.save()

    try:
        entities['discipline']
    except:
        discipline_query = Conversation_bot_context.objects.filter(conversation=id_user,value_type='discipline').values('value')
        if len(discipline_query) > 0:
            discipline = discipline_query[0]['value']
    else:
        discipline = entities['discipline']
        #print('discipline',discipline)
        conversation_context = Conversation_bot_context(conversation=id_user,value_type='discipline',value=discipline)
        conversation_context.save()

    #print('entities__end',entities)

    #print('conveyor_belt',conveyor_belt)
    #print('save_point_insert_problem',save_point_insert_problem)

    if conveyor_belt == '':
        response = "Which convertor belt has the problem? {}, let me help, here is a list of our conveyor belts:".format(user_name)
        context.bot.send_message(chat_id=update.effective_chat.id, text=response)
        for cb in conveyor_belt_list:
            response = cb
            context.bot.send_message(chat_id=update.effective_chat.id, text=response)
    else:
        if machine == '':
            response = "Which machine has the problem? {}, let me help, here is a list of our machines:".format(user_name)
            context.bot.send_message(chat_id=update.effective_chat.id, text=response)
            for m in machine_list:
                response = m
                context.bot.send_message(chat_id=update.effective_chat.id, text=response)
        else:
            #print('failure_mode_int',failure_mode)
            if failure_mode == '':
                response = "What is the failure? {}, let me help, here is a list of our failures:\n".format(user_name)
                context.bot.send_message(chat_id=update.effective_chat.id, text=response)
                for fm in failure_mode_list:
                    response += fm + "\n"
                
                context.bot.send_message(chat_id=update.effective_chat.id, text=response)

    conveyor_belt_1 = ''
    if  conveyor_belt == 'BELT A':
        conveyor_belt_1 = 'A'
    else:
        if conveyor_belt == 'BELT B':
            conveyor_belt_1 = 'B'
        else:
            if conveyor_belt == 'BELT C':
                conveyor_belt_1 = 'C'
            else:
                conveyor_belt_1 = 'D'
    #print('conveyor_belt_end',conveyor_belt_1)
    #print('machine_end',machine)
    #print('failure_mode_end',failure_mode)

    if conveyor_belt != '' and machine != '' and failure_mode != '':
        response = 'OK, problem reported. Technicians will work on it soon'
        avg_time = Failure.objects.filter(conveyor_belt=conveyor_belt_1).all().aggregate(Avg('avg_repair_time'))
        avg_time_value = avg_time['avg_repair_time__avg']
        avg_cost = Failure.objects.filter(conveyor_belt=conveyor_belt_1).all().aggregate(Avg('avg_repair_cost'))
        avg_cost_value = avg_cost['avg_repair_cost__avg']
        context.bot.send_message(chat_id=update.effective_chat.id, text=response)
        response = 'Hummm {}, I estimate the repair will take {} hours and it will cost ${:,.2f}'.format(user_name,ceil(avg_time_value),ceil(avg_cost_value))
        context.bot.send_message(chat_id=update.effective_chat.id, text=response)
        Conversation_bot_context.objects.filter(conversation=id_user).delete()

def view_problem(update,context):
    #problem = 'as'
    effective_user = update['_effective_user']
    id_user = effective_user['id']
    user_name = effective_user['first_name']
    problem = Failure.objects.filter(status='Open').values('failure_mode','avg_repair_time','avg_repair_cost')[0]
    # #print(problem.get('failure_mode'))
    # #print(problem.get('avg_repair_time'))
    if problem == '':
        response = "Congratulations {}, I didn't find any problem in the factory.".format(user_name)
        context.bot.send_message(chat_id=update.effective_chat.id, text=response)
        #user_responde enviar ao watson
        Conversation_bot_context.objects.filter(conversation=id_user).delete()
    else:
        falha = problem.get('failure_mode')
        tempo = ceil(problem.get('avg_repair_time'))
        custo = problem.get("avg_repair_cost")
        response = "Sorry to inform, but we have the following problem:"
        context.bot.send_message(chat_id=update.effective_chat.id, text=response)
        response = "Problem : {}".format(falha)
        context.bot.send_message(chat_id=update.effective_chat.id, text=response)
        response = "Average repair time: {} hour(s)".format(tempo)
        context.bot.send_message(chat_id=update.effective_chat.id, text=response)
        response = "Average repair cost:$ {:,.2f}".format(custo)
        context.bot.send_message(chat_id=update.effective_chat.id, text=response )
        Conversation_bot_context.objects.filter(conversation=id_user).delete()

def pam_help(update,context):
    effective_user = update['_effective_user']
    id_user = effective_user['id']
    user_name = effective_user['first_name']
    response = 'Hi {}, my name is PAM. Your personal Production Assistant Manager.'.format(user_name)
    context.bot.send_message(chat_id=update.effective_chat.id, text=response)
    response = 'I can help you to manage the factory.'
    context.bot.send_message(chat_id=update.effective_chat.id, text=response)
    response = 'If you need things like "insert an order" or "inform a problem" you can call me.'
    context.bot.send_message(chat_id=update.effective_chat.id, text=response)
    response = 'You only need to send me a message like "Hello PAM. I’d like to place an order" and I will help you.'
    context.bot.send_message(chat_id=update.effective_chat.id, text=response)
    Conversation_bot_context.objects.filter(conversation=id_user).delete()

def start_bot():
    print('Starting Telegram Bot...')
    #updater = Updater(token='809750641:AAGoDOgxgnAzhIk3OYfXhWkAfEcgjUmzuPo', use_context=True)
    updater = Updater(token='854619524:AAHPQQmFLzZL5AIPSvr62zHLcnJLI3GfUkk', use_context=True)
    dispatcher = updater.dispatcher

    logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                     level=logging.INFO)
    #handlers
    start_handler = CommandHandler('start', start)

    non_command_handler = MessageHandler(Filters.text, non_command) #always last
    dispatcher.add_handler(start_handler)

    dispatcher.add_handler(non_command_handler) #always last

    #start!
    updater.start_polling()
    return updater

def stop_bot():
    global updater
    updater.stop()
    #updater.idle()

updater = start_bot()

def my_signal_handler(*args):
    if os.environ.get('RUN_MAIN') == 'true':
        print('Stopping Telegram Bot...')
        stop_bot()
    sys.exit(0)

signal.signal(signal.SIGINT, my_signal_handler)
