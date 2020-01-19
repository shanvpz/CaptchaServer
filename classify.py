import tensorflow as tf, sys, os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
image_path = sys.argv[1]
graph_path = 'Capoutput_graph.pb'
labels_path = 'Capoutput_labels.txt'
 
# Read in the image_data
image_data = tf.io.gfile.GFile(image_path, 'rb').read()
 
# Loads label file, strips off carriage return
label_lines = [line.rstrip() for line
    in tf.io.gfile.GFile(labels_path)]
 
# Unpersists graph from file
with tf.io.gfile.GFile(graph_path, 'rb') as f:
    graph_def = tf.compat.v1.GraphDef()
    graph_def.ParseFromString(f.read())
    _ = tf.import_graph_def(graph_def, name='')
 
# Feed the image_data as input to the graph and get first prediction
with tf.compat.v1.Session() as sess:
    softmax_tensor = sess.graph.get_tensor_by_name('final_result:0')
    predictions = sess.run(softmax_tensor,
    {'DecodeJpeg/contents:0': image_data})
    # Sort to show labels of first prediction in order of confidence
    top_k = predictions[0].argsort()[-len(predictions[0]):][::-1]
    for node_id in top_k:
         human_string = label_lines[node_id]
         score = predictions[0][node_id]
         #print('%s (score = %.5f)' % (human_string, score))
    print('<<',label_lines[top_k[0]])
