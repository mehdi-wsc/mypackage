import os
import subprocess
def test_files():
    File1 = os.path.exists("./mypackage_wsc/infra_builder_terraform.py")
    File2 = os.path.exists("./mypackage_wsc/infra_bootstrap.py")
    File3 = os.path.exists("./mypackage_wsc/install_nginx.py")
    assert File1 is True
    assert File2 is True
    assert File3 is True
def test_response():
    infra_bootstrap_response = subprocess.Popen(['python', 'mypackage_wsc/infra_bootstrap.py'],
    stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    test_1 = str(infra_bootstrap_response.communicate()[0])
    assert 'Missing account argument,Wedeployer Can not run without Account' in str(test_1)
    infra_builder_terraform_response = subprocess.Popen(['python', 'mypackage_wsc/infra_builder_terraform.py'],
    stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    test_2 = str(infra_builder_terraform_response.communicate()[0])
    assert 'Missing account argument,Wedeployer Can not run without Account' in str(test_2)
