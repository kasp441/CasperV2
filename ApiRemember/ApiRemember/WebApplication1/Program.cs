using Domain;
using Microsoft.AspNetCore.Mvc;
using Microsoft.EntityFrameworkCore;
using Repo;

var builder = WebApplication.CreateBuilder(args);

// Add services to the container.
// Learn more about configuring Swagger/OpenAPI at https://aka.ms/aspnetcore/swashbuckle
builder.Services.AddEndpointsApiExplorer();
builder.Services.AddSwaggerGen();
builder.Services.AddScoped<IRememberRepo, RememberRepo>();

var connectionString = builder.Configuration.GetConnectionString("DefaultConnection");

var envConnectionString = Environment.GetEnvironmentVariable("CONNECTION_STRING");
if (!string.IsNullOrWhiteSpace(envConnectionString))
{
    connectionString = envConnectionString;
}

//add connection string here
builder.Services.AddDbContext<RememberContext>(options =>
{
    options.UseNpgsql(connectionString, b => b.MigrationsAssembly("WebApplication1"));
});

var app = builder.Build();

//apply migrations if any
using (var scope = app.Services.CreateScope())
{
    var services = scope.ServiceProvider;
    var context = services.GetRequiredService<RememberContext>();

    if (context.Database.GetPendingMigrations != null)
    {
        context.Database.Migrate();

    }
}

// Configure the HTTP request pipeline.
if (app.Environment.IsDevelopment())
{
    app.UseSwagger();
    app.UseSwaggerUI();
}

app.UseHttpsRedirection();

// create crud operations in minimal here

app.MapGet("/GetRemember", async (IRememberRepo repo) =>
{
    return Results.Ok(repo.ReadAllRemember());
});

app.MapPost("/CreateRemember", async (IRememberRepo repo,[FromBody] Reminder reminder) =>
{
    repo.CreateRemember(reminder);
    return Results.Created($"/remember/{reminder.Id}", reminder);
});

app.MapPut("/UpdateRemember", async (IRememberRepo repo, [FromBody] Reminder reminder) =>
{
    repo.UpdateRemember(reminder);
    return Results.NoContent();
});

app.MapDelete("/DeleteRemember/{id}", async (IRememberRepo repo, int id) =>
{
    var existingReminder = repo.ReadRememberById(id);
    if (existingReminder == null)
    {
        return Results.NotFound();
    }
    repo.DeleteRemember(existingReminder);
    return Results.NoContent();
});



app.Run();

