#! /usr/bin/env python

import rospy
import actionlib
import time
import argparse
import logging

import slugs_ros.msg, slugs_ros.srv

#import __init__
import slugs_logging
slugs_logger = logging.getLogger("slugs_logger")

def slugs_init_execution_string_client(node_name, inputs):
    rospy.wait_for_service(node_name+"/slugs_init_execution_string_service")
    try:
        slugs_init_execution = rospy.ServiceProxy(node_name+"/slugs_init_execution_string_service", slugs_ros.srv.SlugsInitExecutionString)
        resp1 = slugs_init_execution(inputs)
        return resp1.current_inputs_outputs
    except rospy.ServiceException, e:
        print "Service call failed: %s"%e

def slugs_init_execution_array_client(node_name, key_list, value_list):
    request = slugs_ros.srv.SlugsInitExecutionArrayRequest()
    print request
    request.init_inputs_outputs_key_array = key_list
    request.init_inputs_outputs_value_array = value_list

    rospy.wait_for_service(node_name+"/slugs_init_execution_array_service")
    try:
        slugs_init_execution = rospy.ServiceProxy(node_name+"/slugs_init_execution_array_service", slugs_ros.srv.SlugsInitExecutionArray)
        resp1 = slugs_init_execution(request)
        return resp1.current_inputs_outputs_key_array, resp1.current_inputs_outputs_value_array
    except rospy.ServiceException, e:
        print "Service call failed: %s"%e


def slugs_trans_execution_string_client(node_name, inputs):
    rospy.wait_for_service(node_name+"/slugs_trans_execution_string_service")
    try:
        slugs_trans_execution = rospy.ServiceProxy(node_name+"/slugs_trans_execution_string_service", slugs_ros.srv.SlugsTransExecutionString)
        resp1 = slugs_trans_execution(inputs)
        return resp1.current_inputs_outputs
    except rospy.ServiceException, e:
        print "Service call failed: %s"%e

def slugs_trans_execution_array_client(node_name, key_list, value_list):
    request = slugs_ros.srv.SlugsTransExecutionArrayRequest()
    request.trans_inputs_key_array = key_list
    request.trans_inputs_value_array = value_list

    rospy.wait_for_service(node_name+"/slugs_trans_execution_array_service")
    try:
        slugs_trans_execution = rospy.ServiceProxy(node_name+"/slugs_trans_execution_array_service", slugs_ros.srv.SlugsTransExecutionArray)
        resp1 = slugs_trans_execution(request)
        return resp1.current_inputs_outputs_key_array, resp1.current_inputs_outputs_value_array
    except rospy.ServiceException, e:
        print "Service call failed: %s"%e

def slugs_set_goal_client(node_name, inputs):
    rospy.wait_for_service(node_name+"/slugs_set_goal_service")
    try:
        slugs_trans_execution = rospy.ServiceProxy(node_name+"/slugs_set_goal_service", slugs_ros.srv.SlugsSetGoal)
        resp1 = slugs_trans_execution(inputs)
        return resp1.current_goal_id
    except rospy.ServiceException, e:
        print "Service call failed: %s"%e

def slugs_get_inputs_client(node_name):
    rospy.wait_for_service(node_name+"/slugs_get_inputs_service")
    try:
        slugs_get_inputs = rospy.ServiceProxy(node_name+"/slugs_get_inputs_service", slugs_ros.srv.SlugsGetInputs)
        resp1 = slugs_get_inputs()
        return resp1.inputs_array
    except rospy.ServiceException, e:
        print "Service call failed: %s"%e

def slugs_get_outputs_client(node_name):
    rospy.wait_for_service(node_name+"/slugs_get_outputs_service")
    try:
        slugs_get_outputs = rospy.ServiceProxy(node_name+"/slugs_get_outputs_service", slugs_ros.srv.SlugsGetOutputs)
        resp1 = slugs_get_outputs()
        return resp1.outputs_array
    except rospy.ServiceException, e:
        print "Service call failed: %s"%e

def slugs_feedback(msg):
    print '-------------------------------------'
    print "Feedback from slugs synthesis:\n" + str(msg)
    print '-------------------------------------'

def start_slugs_action_client(node_name, ltl_filename, synthesis_options):
    """
    This function start the slugs action server.
    @param node_name: name of the slugs node
    @type  node_name: string
    @param ltl_filename: name of the slugsin file
    @type  ltl_filename: string
    @param synthesis_options: options for slugs synthesis
    @type  synthesis_options: list

    @return: results from slugs synthesis
    @rtype: slugs_ros.msg.SlugsSynthesisResult()
    """
    client = actionlib.SimpleActionClient(node_name+"/slugs_synthesis_action", slugs_ros.msg.SlugsSynthesisAction)
    slugs_logger.info("Waiting for server")
    client.wait_for_server()

    # send slugsin file
    goal = slugs_ros.msg.SlugsSynthesisGoal()
    goal.ltl_filename = ltl_filename
    #goal.output_filename = args.ltl_filename.replace('.slugsin','.aut')
    goal.options = synthesis_options

    # Fill in the goal here
    client.send_goal(goal,feedback_cb=slugs_feedback)
    if client.get_goal_status_text():
        slugs_logger.debug(client.get_goal_status_text())
    client.wait_for_result()
    result = client.get_result()
    slugs_logger.info(result)
    return result


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Slugs Request Helper."+ \
        "Note that the current testscript is only designed for the firefighting example.")
    #parser.add_argument('ltl_filename', type=str, help='Specify .slugsin for now')
    #parser.add_argument('server_node_name', type=str, help='Specify name of server.')

    args = parser.parse_args()

    server_name = 'slugs_server'
    rospy.init_node('test_slugs_client')
    client = actionlib.SimpleActionClient(server_name+"/slugs_synthesis_action", slugs_ros.msg.SlugsSynthesisAction)
    client.wait_for_server()

    goal = slugs_ros.msg.SlugsSynthesisGoal()
    goal.ltl_filename = "/home/catherine/LTLMoP/src/examples/firefighting/firefighting.slugsin"
    #goal.ltl_filename = args.ltl_filename
    #goal.output_filename = args.ltl_filename.replace('.slugsin','.aut')
    goal.options = ["--interactiveStrategy"]


    # Fill in the goal here
    client.send_goal(goal,feedback_cb=slugs_feedback)
    print client.get_goal_status_text()
    client.wait_for_result()#rospy.Duration.from_sec(5.0))
    result = client.get_result()
    print result

    while not rospy.is_shutdown():
        ### test service #####
        print  "Init_state_string:" + slugs_init_execution_string_client(server_name, "")

        init_key = ['person']
        init_value = [True]
        key, value = slugs_init_execution_array_client(server_name, init_key, init_value)
        print  "Init_state_key:" + str(key)
        print  "Init_state_value:" + str(value)

        print  "Init_state_string:" + slugs_init_execution_string_client(server_name, "000000...")

        print  "Trans_state_string:" + str(slugs_trans_execution_string_client(server_name, "00"))
        print  "Trans_state_string:" + str(slugs_trans_execution_string_client(server_name, "10"))

        trans_key = ['person', 'hazardous_item']
        trans_value = [True, False]
        key, value = slugs_trans_execution_array_client(server_name, trans_key, trans_value)
        print  "Trans_state_key:" + str(key)
        print  "Trans_state_value:" + str(value)

        trans_value = [False, True]
        key, value = slugs_trans_execution_array_client(server_name, trans_key, trans_value)
        print  "Trans_state_key:" + str(key)
        print  "Trans_state_value:" + str(value)

        print  "Set current goal to:" + str(slugs_set_goal_client(server_name, 0))

        print "Input list: {0}".format(slugs_get_inputs_client(server_name))
        print "Output list: {0}".format(slugs_get_outputs_client(server_name))
