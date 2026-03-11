package ru.hse.profiling;

import ru.hse.Account;
import ru.hse.OperationException;
import ru.hse.client.Client;
import ru.hse.server.Server;

public final class ServerProfilingLoadTest {
    private static final int DEFAULT_PORT = 7001;
    private static final int DEFAULT_ITERATIONS = 300_000;

    private ServerProfilingLoadTest() {
    }

    public static void main(String[] args) throws Exception {
        int iterations = DEFAULT_ITERATIONS;
        int port = DEFAULT_PORT;

        if (args.length > 0) {
            iterations = Integer.parseInt(args[0]);
        }
        if (args.length > 1) {
            port = Integer.parseInt(args[1]);
        }

        Server server = new Server();
        server.start(port);
        server.waitStarted();

        String url = "http://localhost:" + port;
        Client client = new Client(url);
        String runId = Long.toString(System.currentTimeMillis());

        int succeeded = 0;
        int failed = 0;

        try {
            for (int i = 0; i < iterations; i++) {
                String login = "profile_user_" + runId + "_" + i;
                String password = "pwd_" + i;

                try {
                    Account account = client.register(login, password);
                    if (account == null) {
                        failed++;
                        continue;
                    }
                    Client.deposit(account, 100);
                    try {
                        Client.withdraw(account, 200);
                    } catch (OperationException ignored) {
                        // expected for insufficient funds in part of iterations
                    }
                    Client.withdraw(account, 50);
                    client.logout(account);
                    succeeded++;
                } catch (OperationException e) {
                    failed++;
                }

                if (i % 10 == 0) {
                    try {
                        client.login(login, password + "_wrong");
                    } catch (OperationException ignored) {
                        // intentional failed auth attempt
                    }
                }
            }
        } finally {
            server.stop();
        }

        System.out.println("Load finished. succeeded=" + succeeded + ", failed=" + failed);
    }
}
