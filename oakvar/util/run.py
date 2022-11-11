def update_status(status: str, logger=None, serveradmindb=None):
    if logger:
        logger.info(status)
    if serveradmindb:
        serveradmindb.update_job_info({"status": status})


def announce_module(module, logger=None, serveradmindb=None):
    update_status(
        "Running {name}".format(name=module.name),
        logger=logger,
        serveradmindb=serveradmindb,
    )


def log_variant_exception(
    lnum=0,
    line="",
    __input_data__=None,
    unique_excs=[],
    logger=None,
    error_logger=None,
    e=None,
):
    import traceback

    if logger:
        err_str = traceback.format_exc().rstrip()
        if err_str.endswith("None"):
            err_str_log = str(e)
        else:
            err_str_log = err_str
        if not err_str_log in unique_excs:
            unique_excs.append(err_str_log)
            logger.error(err_str_log)
    if error_logger:
        error_logger.error("\n[{:d}]{}\n({})\n#".format(lnum, line.rstrip(), str(e)))


def print_log_handlers():
    import logging

    for k, v in logging.Logger.manager.loggerDict.items():
        if "oakvar" in k:
            print("+ [%s] {%s} " % (str.ljust(k, 20), str(v.__class__)[8:-2]))
            if not isinstance(v, logging.PlaceHolder):
                for h in v.handlers:
                    print("     +++", str(h.__class__)[8:-2])
                    for fld, val in h.__dict__.items():
                        print("%s%s=%s" % ("   -", fld, val))


def get_y_or_n():
    while True:
        resp = input("Proceed? ([y]/n) > ")
        if resp == "y" or resp == "":
            return True
        if resp == "n":
            return False
        else:
            continue


def show_logo():
    print(
        r"""
==========================================================
 #######     ###    ##    ## ##     ##    ###    ########  
##     ##   ## ##   ##   ##  ##     ##   ## ##   ##     ## 
##     ##  ##   ##  ##  ##   ##     ##  ##   ##  ##     ## 
##     ## ##     ## #####    ##     ## ##     ## ########  
##     ## ######### ##  ##    ##   ##  ######### ##   ##   
##     ## ##     ## ##   ##    ## ##   ##     ## ##    ##  
 #######  ##     ## ##    ##    ###    ##     ## ##     ##
==========================================================
                                   Oak Bioinformatics, LLC
              Licensed under AGPL-3 and commercial license
        Licensing and feedback: info@oakbioinformatics.com
                                        https://oakvar.com
""",
        flush=True,
    )
