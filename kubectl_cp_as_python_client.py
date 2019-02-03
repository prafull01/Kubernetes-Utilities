"""
The functions currently only support the copying of file from pod and into the pod. Support for copying the entire directory is 
yet to be added
"""


def copy_file_inside_pod(pod_name, src_path, dest_path, namespace='default'):
    """
    This function copies a file inside the pod
    :param api_instance: coreV1Api()
    :param name: pod name
    :param ns: pod namespace
    :param source_file: Path of the file to be copied into pod
    :return: nothing
    """

    api_instance = get_k8s_client_corev1()
    try:
        exec_command = ['tar', 'xvf', '-', '-C', '/']
        api_response = stream(api_instance.connect_get_namespaced_pod_exec, pod_name, namespace,
                              command=exec_command,
                              stderr=True, stdin=True,
                              stdout=True, tty=False,
                              _preload_content=False)

        with TemporaryFile() as tar_buffer:
            with tarfile.open(fileobj=tar_buffer, mode='w') as tar:
                tar.add(src_path, dest_path)

            tar_buffer.seek(0)
            commands = []
            commands.append(tar_buffer.read())

            while api_response.is_open():
                api_response.update(timeout=1)
                if api_response.peek_stdout():
                    print("STDOUT: %s" % api_response.read_stdout())
                if api_response.peek_stderr():
                    print("STDERR: %s" % api_response.read_stderr())
                if commands:
                    c = commands.pop(0)
                    api_response.write_stdin(c.decode())
                else:
                    break
            api_response.close()
    except ApiException as e:
        print("Exception when copying file to the pod%s \n" % e)


def copy_file_from_pod(pod_name, src_path, dest_path, namespace="default"):
    """
    
    :param pod_name: 
    :param src_path: 
    :param dest_path: 
    :param namespace: 
    :return: 
    """

    api_instance = get_k8s_client_corev1()
    exec_command = ['tar', 'cf', '-', src_path]

    with TemporaryFile() as tar_buffer:
        resp = stream(api_instance.connect_get_namespaced_pod_exec, pod_name, namespace,
                      command=exec_command,
                      stderr=True, stdin=True,
                      stdout=True, tty=False,
                      _preload_content=False)

        while resp.is_open():
            resp.update(timeout=1)
            if resp.peek_stdout():
                out = resp.read_stdout()
                # print("STDOUT: %s" % len(out))
                tar_buffer.write(out.encode('utf-8'))
            if resp.peek_stderr():
                print("STDERR: %s" % resp.read_stderr())
        resp.close()

        tar_buffer.flush()
        tar_buffer.seek(0)

        with tarfile.open(fileobj=tar_buffer, mode='r:') as tar:
            for member in tar.getmembers():
                if member.isdir():
                    continue
                fname = member.name.rsplit('/', 1)[1]
                tar.makefile(member, dest_path + '/' + fname)
