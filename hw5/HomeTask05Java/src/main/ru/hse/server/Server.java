package ru.hse.server;

import java.util.Scanner;
import java.util.concurrent.atomic.AtomicBoolean;

public class Server {
    ServerStorage storage = null;
    ServerLogicProxy storageProxy = null;
    AccountServer accountServer = null;
    ApiServer apiServer = null;
    AccountSecurity accountSecurity = null;

    public void start(int port) {
        storage = new ServerStorage("accounts");
        storageProxy = new ServerLogicProxy(storage);
        accountServer = new AccountServer(storage, storageProxy);
        // security server, tends to be active only when accounts are logged
        accountSecurity = new AccountSecurity(accountServer, storage);
        apiServer = new ApiServer(accountServer, port);

        storage.setChangeVerifier(accountSecurity);
        apiServer.addAuthListener(accountSecurity);
    }

    public void stop() {
        if (apiServer != null) {
            apiServer.stop();
        }
        if (storage != null) {
            storage.close();
        }
    }

    public static void main(String[] args) {
        Server s = new Server();
        int port = 7000;
        if (args.length>0)
            try{
                port = Integer.parseInt(args[0]);
            }catch(NumberFormatException ignore){
                // keep default port
            }
        s.start(port);

        Scanner scanner = new Scanner(System.in);

        System.out.print("Enter stop to stop a server: ");
        while (!"stop".equals(scanner.nextLine().trim())) {
            System.out.print("Wrong command, enter stop to stop a server:");
        }
        s.stop();
    }

    public void waitStarted() {
        while (!apiServer.isStarted) {
            synchronized (apiServer) {
                try {
                    apiServer.wait(500);
                } catch (InterruptedException ignored) {
                }
            }
        }
    }
}
